from django.urls import path
from .views import LoginAPIView, UserDeleteView, UserDetailsView, UserSignupView, UserUpdateView#UserUpdateView
# from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/user_detail/<int:id>/', UserDetailsView.as_view(), name='user-details'),
    path('api/user_update/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('api/user_delete/<int:id>/', UserDeleteView.as_view(), name='user-delete'),
]
