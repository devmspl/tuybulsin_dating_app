from django.urls import path
from .views import LikeProfileAPIView, DislikeProfileAPIView, LikedProfilesAPIView, RandomProfileView

urlpatterns = [
    path('like/<int:pk>/', LikeProfileAPIView.as_view(), name='like_profile'),
    path('dislike/<int:pk>/', DislikeProfileAPIView.as_view(), name='dislike_profile'),
    path('liked/', LikedProfilesAPIView.as_view(), name='liked_profiles'),
    path('random-profile/', RandomProfileView.as_view(), name='random_profile'),
]