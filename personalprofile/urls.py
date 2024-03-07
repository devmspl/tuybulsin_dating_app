from django.urls import path
from .views import ImageUploadAPIView, ProfileCreateAPIView, ProfileUpdateAPIView

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
]