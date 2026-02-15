from django.db import models
from django.conf import settings
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile

# -------------------------------
# User Profile
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# -------------------------------
# Secure File Field Helper
# -------------------------------
class EncryptedFileField(models.FileField):
    """
    Custom FileField that encrypts file content using Fernet before saving.
    """

    def save_form_data(self, instance, data):
        if data:
            key = settings.FERNET_KEY
            fernet = Fernet(key)
            file_content = data.read()
            encrypted_content = fernet.encrypt(file_content)
            encrypted_file = ContentFile(encrypted_content, name=data.name)
            super().save_form_data(instance, encrypted_file)
        else:
            super().save_form_data(instance, data)

    def open(self, mode='rb'):
        key = settings.FERNET_KEY
        fernet = Fernet(key)
        original_file = super().open(mode)
        encrypted_content = original_file.read()
        decrypted_content = fernet.decrypt(encrypted_content)
        return ContentFile(decrypted_content, name=self.name)


# -------------------------------
# Document Model
# -------------------------------
class Document(models.Model):
    DOC_TYPES = [
        ('CV', 'Curriculum Vitae'),
        ('Passport', 'Passport'),
        ('ID', 'ID Card'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    title = EncryptedCharField(max_length=255)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default='Other')
    description = EncryptedTextField(blank=True)

    # Secure file field
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.doc_type})"


# -------------------------------
# Document Sharing Model
# -------------------------------
class DocumentShare(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='shares')
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_docs')
    token = EncryptedCharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    can_download = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Share of {self.document.title} with {self.shared_with.username}"
