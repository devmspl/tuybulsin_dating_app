from django.urls import path
from .views import LikeProfileAPIView, DislikeProfileAPIView, LikedProfileByProfileId, LikedProfileByUserId, LikedProfilesAPIView, RandomProfileView

urlpatterns = [
    path('like/<int:pk>/', LikeProfileAPIView.as_view(), name='like_profile'),
    path('dislike/<int:pk>/', DislikeProfileAPIView.as_view(), name='dislike_profile'),
    path('liked/', LikedProfilesAPIView.as_view(), name='liked_profiles'),
    path('random-profile/', RandomProfileView.as_view(), name='random_profile'),
    path('liked-profiles/user/<int:user_id>/', LikedProfileByUserId.as_view(), name='liked-profiles-by-user'),
    path('liked-profiles/<int:profile_id>/', LikedProfileByProfileId.as_view(), name='liked-profiles-by-profile'),
]