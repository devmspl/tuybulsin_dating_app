from django import views
from django.urls import path
from .views import AudioDeleteAPIView, AudioUploadAPIView, CancelPlanView, GetUserPreferenceAPIView, ImageDeleteAPIView, ImageUploadAPIView, PlanAPIView, ProfileCreateAPIView, ProfileRetrieveAPIView, ProfileUpdateAPIView, PurchasePlanView, SetUserPreferenceAPIView, UpdateUserPreferenceAPIView, UpdateUserPreferenceLatLong

urlpatterns = [
    path('create/', ProfileCreateAPIView.as_view(), name='profile_create'),
    path('getprofile/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='profile_retrieve'),
    path('update/<int:pk>/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('upload/', ImageUploadAPIView.as_view(), name='image_upload'),
    path('imagedelete/', ImageDeleteAPIView.as_view(), name='image-delete'),
    path('setpreference/<int:user_id>/', SetUserPreferenceAPIView.as_view(), name='set_preference'),
    path('updatepreference/', UpdateUserPreferenceAPIView.as_view(), name='update_preference'),
    path('getpreference/', GetUserPreferenceAPIView.as_view(), name='get_preference'),
    path('api/plan/<int:user_id>/', PlanAPIView.as_view(), name='plan'),
    path('purchase/<int:user_id>/<int:plan_id>/', PurchasePlanView.as_view(), name='purchase-plan'),
    path('cancel/<int:user_id>/<int:plan_id>/', CancelPlanView.as_view(), name='cancel-plan'),
    path('update-lat-long/', UpdateUserPreferenceLatLong.as_view(), name='update_lat_long'),
    path('audioupload/', AudioUploadAPIView.as_view(), name='audio_upload'),
    path('audio/delete/', AudioDeleteAPIView.as_view(), name='audio_delete'),
   
]
    
