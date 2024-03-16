from django import views
from django.urls import path
from .views import ImageUploadAPIView, PersonalInformationFilterAPIView, PlanAPIView, ProfileCreateAPIView, ProfileRetrieveAPIView, ProfileUpdateAPIView

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('getprofile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_retrieve'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
    path('setpreference/', PersonalInformationFilterAPIView.as_view(), name='filter_profiles'),
    path('api/plan/<int:user_id>/', PlanAPIView.as_view(), name='plan'),
]