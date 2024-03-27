from django.urls import include, path
from . import views

urlpatterns = [
    path('userlist/', views.user_list, name='user_list'),
    path('message/', views.MessageSendAPIView.as_view()),
    path('messages/<int:sender_id>/<int:recipient_id>/', views.MessageGetAPIView.as_view(), name='messages'),
    path('messages/<int:message_id>/<int:sender_id>/<int:recipient_id>/delete/', views.MessageGetAPIView.as_view(), name='delete_messages'),
    
]
