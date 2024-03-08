from django.urls import path
from .views import LikeProfileAPIView, DislikeProfileAPIView, LikedProfilesAPIView

urlpatterns = [
    path('like/<int:pk>/', LikeProfileAPIView.as_view(), name='like_profile'),
    path('dislike/<int:pk>/', DislikeProfileAPIView.as_view(), name='dislike_profile'),
    path('liked/', LikedProfilesAPIView.as_view(), name='liked_profiles'),
]