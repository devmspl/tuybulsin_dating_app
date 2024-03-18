from django import views
from django.urls import path
from .views import ImageUploadAPIView, PlanAPIView, ProfileCreateAPIView, ProfileRetrieveAPIView, ProfileUpdateAPIView, SetUserPreferenceAPIView

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('getprofile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_retrieve'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
     path('setpreference/', SetUserPreferenceAPIView.as_view(), name='set_preference'),
    path('api/plan/<int:user_id>/', PlanAPIView.as_view(), name='plan'),
]