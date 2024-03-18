from django import views
from django.urls import path
from .views import GetUserPreferenceAPIView, ImageUploadAPIView, PlanAPIView, ProfileCreateAPIView, ProfileRetrieveAPIView, ProfileUpdateAPIView, SetUserPreferenceAPIView, UpdateUserPreferenceAPIView

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('getprofile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_retrieve'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
    path('setpreference/<int:user_id>/', SetUserPreferenceAPIView.as_view(), name='set_preference'),
    path('updatepreference/', UpdateUserPreferenceAPIView.as_view(), name='update_preference'),
    path('getpreference/', GetUserPreferenceAPIView.as_view(), name='get_preference'),
    path('api/plan/<int:user_id>/', PlanAPIView.as_view(), name='plan'),
    
]