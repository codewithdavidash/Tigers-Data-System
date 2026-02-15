from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *
from .forms import LoginForm

urlpatterns = [
    # Dashboard / home
    path('', index, name='index'),

    # Login
    path(
        'accounts/login/',
        LoginView.as_view(
            authentication_form=LoginForm,
            template_name='auth/login.html'
        ),
        name='login'
    ),

    # Logout
    path('accounts/logout/', logoutView, name='logout'),

    # Register
    path('accounts/register/', register, name='register'),
    path('documents/share/<int:doc_id>/', share_document, name='share_document'),
    path('documents/download/<int:doc_id>/', download_document, name='download_document'),
    path('documents/upload/', upload_document, name='upload_document'),
]
