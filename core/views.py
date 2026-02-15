from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from cryptography.fernet import Fernet
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from io import BytesIO
from .models import *
from .forms import *
import uuid

# -------------------------------
# Dashboard / Index
# -------------------------------
@login_required
def index(request):
    # Your owned documents
    recent_docs = Document.objects.filter(owner=request.user).order_by('-uploaded_at')
    
    # Documents shared WITH you by others (that haven't expired)
    shared_with_me = DocumentShare.objects.filter(
        shared_with=request.user,
        expires_at__gt=timezone.now(),
        can_download=True
    ).select_related('document', 'document__owner')
    
    context = {
        'recent_docs': recent_docs,
        'shared_with_me': shared_with_me
    }
    return render(request, 'core/index.html', context)


@login_required
def revoke_access(request, share_id):
    # Find the share record, but only if the document belongs to the current user
    share = get_object_or_404(DocumentShare, id=share_id, document__owner=request.user)
    
    target_user = share.shared_with.username
    doc_title = share.document.title
    
    share.delete()
    
    messages.success(request, f"Access revoked for {target_user} on asset: {doc_title}")
    return redirect('index')

# -------------------------------
# Secure Document Download
# -------------------------------
from django.db.models import Q

@login_required
def download_document(request, doc_id):
    # 1. Fetch the document regardless of owner first
    doc = get_object_or_404(Document, id=doc_id)

    # 2. Check Permissions: User must be owner OR have a valid share
    is_owner = doc.owner == request.user
    
    has_active_share = DocumentShare.objects.filter(
        document=doc,
        shared_with=request.user,
        expires_at__gt=timezone.now(),
        can_download=True
    ).exists()

    if not (is_owner or has_active_share):
        messages.error(request, "You do not have permission to download this file or the link has expired.")
        return redirect('index')

    # 3. Process Decryption
    fernet = Fernet(settings.FERNET_KEY)
    try:
        # Accessing storage directly is often more reliable for encrypted custom fields
        with doc.file.open('rb') as f:
            content = f.read()
            
        if not content:
            raise Http404("The file is empty on the server.")

        decrypted_content = fernet.decrypt(content)

        # 4. Update Statistics
        doc.downloads += 1
        doc.save(update_fields=['downloads'])

        # 5. Build Response
        response = FileResponse(BytesIO(decrypted_content), as_attachment=True)
        
        # Clean up filename (removes the date folders from the download name)
        clean_filename = doc.file.name.split("/")[-1]
        response['Content-Disposition'] = f'attachment; filename="{clean_filename}"'
        response['Content-Length'] = len(decrypted_content)
        
        return response

    except Exception as e:
        print(f"Decryption Error: {e}")
        messages.error(request, "Decryption failed. File may be corrupted or key changed.")
        return redirect('index')
# -------------------------------
# Logout
# -------------------------------
@login_required
def logoutView(request):
    logout(request)
    messages.info(request, "Your Session Has Ended!")
    return redirect('login')


# -------------------------------
# Register
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Has Been Created!")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


# -------------------------------
# Upload Document (Encrypted)
# -------------------------------

@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            filename = uploaded_file.name

            # 🔒 Encrypt
            fernet = Fernet(settings.FERNET_KEY)
            raw_bytes = uploaded_file.read() 
            encrypted_bytes = fernet.encrypt(raw_bytes)

            # 🧱 Create the object without saving to DB yet
            doc = Document(
                owner=request.user,
                title=form.cleaned_data["title"],
                doc_type=form.cleaned_data.get("doc_type"),
                description=form.cleaned_data.get("description"),
            )

            # 💾 Save using ContentFile (more reliable for S3/Storage backends)
            # This automatically handles the pointer/seek logic for you
            doc.file.save(filename, ContentFile(encrypted_bytes), save=True)

            messages.success(request, "Document uploaded securely.")
            return redirect("index")
    else:
        form = DocumentUploadForm()
    return render(request, "core/upload_document.html", {"form": form})
  

@login_required
def share_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, owner=request.user)
    
    if request.method == "POST":
        shared_user_id = request.POST.get("shared_with")
        shared_user = get_object_or_404(User, id=shared_user_id)
        
        # Create the share record
        share = DocumentShare.objects.create(
            document=doc,
            shared_with=shared_user,
            token=str(uuid.uuid4()), # Unique ID for the link
            expires_at=timezone.now() + timedelta(days=2), # Valid for 2 days
            can_download=True
        )
        
        messages.success(request, f"Access granted to {shared_user.username} for 48 hours.")
        return redirect('index')
    
    # Get all users except the owner to show in a dropdown
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'core/share_document.html', {'doc': doc, 'users': users})