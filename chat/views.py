# # from django.shortcuts import get_object_or_404, render

# # # Create your views here.
# # # https://chat.openai.com/c/9d57e375-ce04-4915-aee7-33995e651c6b
# # #https://bdvade.hashnode.dev/building-chat-apis-with-django-rest-framework-and-django-channels

# from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# from user_management.models import CustomUser 
# from .serializers import  MessageSerializer, UserSerializer
# # from django.db.models import Q
# # from django.shortcuts import redirect, reverse
# # from django.contrib.auth.decorators import login_required
# # from rest_framework.authtoken.models import Token
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated

# @api_view(['GET'])
# def user_list(request, ):
#     users = CustomUser.objects.all().order_by('username')
#     serializer = UserSerializer(instance=users, many=True)
#     return Response(serializer.data)


# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# User = get_user_model()
# from .models import Message


# # class MessageSendAPIView(APIView):
# #     permission_classes = (IsAuthenticated,)

# #     def get(self, request):
# #         channel_layer = get_channel_layer()
# #         async_to_sync(channel_layer.group_send)(
# #             "general", {"type": "send_info_to_user_group",
# #                         "text": {"status": "done"}}
# #         )

# #         return Response({"status": True}, status=status.HTTP_200_OK)

# #     def post(self, request):
# #         msg = Message.objects.create(user=request.user, message={
# #                                      "message": request.data["message"]})
# #         socket_message = f"Message with id {msg.id} was created!"
# #         channel_layer = get_channel_layer()
# #         async_to_sync(channel_layer.group_send)(
# #             f"{request.user.id}-message", {"type": "send_last_message",
# #                                            "text": socket_message}
# #         )

# #         return Response({"status": True}, status=status.HTTP_201_CREATED)
# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = '__all__'


# class MessageSendAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         # This method can be used to send a message to a specific user or group
#         # Here, we are sending a message to the "general" group as an example
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "general", {"type": "send_info_to_user_group",
#                         "text": {"status": "done"}}
#         )

#         return Response({"status": True}, status=status.HTTP_200_OK)

#     def post(self, request):
#         recipient_id = request.data.get("recipient_id")
#         if not recipient_id:
#             return Response({"error": "Recipient ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         recipient = User.objects.filter(id=recipient_id).first()
#         if not recipient:
#             return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)

#         msg = Message.objects.create(sender=request.user, recipient=recipient, message=request.data.get("message"))
#         socket_message = f"Message with id {msg.id} was created!"

#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"chat_{request.user.id}", {"type": "send_message",
#                                         "message": msg.message,
#                                         "timestamp": msg.timestamp,
#                                         "sender_id": request.user.id,
#                                         "recipient_id": recipient_id,
#                                         'text':socket_message}
#         )
#         async_to_sync(channel_layer.group_send)(
#             f"chat_{recipient_id}", {"type": "send_message",
#                                       "message": msg.message,
#                                       "timestamp": msg.timestamp,
#                                       "sender_id": request.user.id,
#                                       "recipient_id": recipient_id,
#                                       'text':socket_message}
#         )

#         return Response({"status": True}, status=status.HTTP_201_CREATED)

# class MessageGetAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request,sender_id, recipient_id):
#         # This method can be used to send a message to a specific user or group
#         # Here, we are sending a message to the "general" group as an example
#         messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id)
#         serializer = MessageSerializer(messages, many=True)
#         return Response({"status": True,'data':serializer.data}, status=status.HTTP_200_OK)


#     # def delete(self, request, sender_id, recipient_id):
#     #     messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id)
#     #     messages.delete()
#     #     return Response({"status": True, 'message': 'Messages deleted successfully'}, status=status.HTTP_200_OK)
#     def delete(self, request, message_id,sender_id, recipient_id):
#         try:
#             message = Message.objects.get(id=message_id, sender_id=sender_id, recipient_id=recipient_id)
#             message.delete()
#             return Response({"status": True, 'message': 'Message deleted successfully'}, status=status.HTTP_200_OK)
#         except Message.DoesNotExist:
#             return Response({"status": False, 'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)