from django.contrib import admin
from .models import UserProfile, Document, DocumentShare

# -------------------------------
# UserProfile Admin
# -------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'country')
    search_fields = ('user__username', 'phone_number', 'country')
    list_filter = ('country',)


# -------------------------------
# Document Admin
# -------------------------------
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'doc_type', 'uploaded_at', 'downloads')
    search_fields = ('title', 'description', 'owner__username')
    list_filter = ('doc_type', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'downloads')


# -------------------------------
# DocumentShare Admin
# -------------------------------
@admin.register(DocumentShare)
class DocumentShareAdmin(admin.ModelAdmin):
    list_display = ('document', 'shared_with', 'can_download', 'expires_at', 'created_at')
    search_fields = ('document__title', 'shared_with__username', 'token')
    list_filter = ('can_download', 'expires_at')
    readonly_fields = ('created_at',)
