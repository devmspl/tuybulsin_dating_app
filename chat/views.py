# from django.shortcuts import get_object_or_404, render

# # Create your views here.
# # https://chat.openai.com/c/9d57e375-ce04-4915-aee7-33995e651c6b
# #https://bdvade.hashnode.dev/building-chat-apis-with-django-rest-framework-and-django-channels
# from rest_framework import status
# from django.shortcuts import render
# from .models import Message
# from .models import Conversation
from rest_framework.decorators import api_view
# from rest_framework.response import Response
from user_management.models import CustomUser 
from .serializers import  MessageSerializer, UserSerializer
# from django.db.models import Q
# from django.shortcuts import redirect, reverse
# from django.contrib.auth.decorators import login_required
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def user_list(request, ):
    users = CustomUser.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)

# # Create your views here.

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def start_convo(request, ):
#     data = request.data
#     print('data',data)
#     try:
#         token = Token.objects.get(user=request.user)
#         print('token',token)
#         user = token.user
#         print('user1',user)
#     except Token.DoesNotExist:
#             # Handle token not found or invalid token
#             pass
#     print('request user',request.user)
#     email = data.pop('email')
#     # # user_id = get_object_or_404(User, email=email).id
#     # user = get_object_or_404(CustomUser, email=email)
#     # print('user',user)
#     # if not user.is_authenticated:
#     #     return Response({"message": "Only authenticated users can start a conversation."},status=status.HTTP_401_UNAUTHORIZED)
#     try:
#         participant = CustomUser.objects.get(email=email)
#         # participant = get_object_or_404(User, email=email)
#         print('participant',participant)
#     except CustomUser.DoesNotExist:
#         return Response({'message': 'You cannot chat with a non existent user'})

#     conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
#                                                Q(initiator=participant, receiver=request.user))
#     if conversation.exists():
#         print('exists')
#         message = Message.objects.create(conversation=conversation, text=text, sender=request.user)
#         serializer = MessageSerializer(instance=message)
#         return redirect(reverse('get_conversation', args=(conversation[0].id,)))
#     else:
#         conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
#         return Response(ConversationSerializer(instance=conversation).data)


# @api_view(['GET'])
# def get_conversation(request, convo_id):
#     conversation = Conversation.objects.filter(id=convo_id)
#     if not conversation.exists():
#         return Response({'message': 'Conversation does not exist'})
#     else:
#         serializer = ConversationSerializer(instance=conversation[0])
#         return Response(serializer.data)


# @api_view(['GET'])
# def conversations(request):
#     conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
#                                                     Q(receiver=request.user))
#     serializer = ConversationListSerializer(instance=conversation_list, many=True)
#     return Response(serializer.data)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()
from .models import Message


# class MessageSendAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "general", {"type": "send_info_to_user_group",
#                         "text": {"status": "done"}}
#         )

#         return Response({"status": True}, status=status.HTTP_200_OK)

#     def post(self, request):
#         msg = Message.objects.create(user=request.user, message={
#                                      "message": request.data["message"]})
#         socket_message = f"Message with id {msg.id} was created!"
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"{request.user.id}-message", {"type": "send_last_message",
#                                            "text": socket_message}
#         )

#         return Response({"status": True}, status=status.HTTP_201_CREATED)
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageSendAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # This method can be used to send a message to a specific user or group
        # Here, we are sending a message to the "general" group as an example
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "general", {"type": "send_info_to_user_group",
                        "text": {"status": "done"}}
        )

        return Response({"status": True}, status=status.HTTP_200_OK)

    def post(self, request):
        recipient_id = request.data.get("recipient_id")
        if not recipient_id:
            return Response({"error": "Recipient ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        recipient = User.objects.filter(id=recipient_id).first()
        if not recipient:
            return Response({"error": "Recipient not found"}, status=status.HTTP_404_NOT_FOUND)

        msg = Message.objects.create(sender=request.user, recipient=recipient, message=request.data.get("message"))
        socket_message = f"Message with id {msg.id} was created!"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{request.user.id}", {"type": "send_message",
                                        "message": msg.message,
                                        "timestamp": msg.timestamp,
                                        "sender_id": request.user.id,
                                        "recipient_id": recipient_id,
                                        'text':socket_message}
        )
        async_to_sync(channel_layer.group_send)(
            f"chat_{recipient_id}", {"type": "send_message",
                                      "message": msg.message,
                                      "timestamp": msg.timestamp,
                                      "sender_id": request.user.id,
                                      "recipient_id": recipient_id,
                                      'text':socket_message}
        )

        return Response({"status": True}, status=status.HTTP_201_CREATED)

class MessageGetAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,sender_id, recipient_id):
        # This method can be used to send a message to a specific user or group
        # Here, we are sending a message to the "general" group as an example
        messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({"status": True,'data':serializer.data}, status=status.HTTP_200_OK)


    # def delete(self, request, sender_id, recipient_id):
    #     messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id)
    #     messages.delete()
    #     return Response({"status": True, 'message': 'Messages deleted successfully'}, status=status.HTTP_200_OK)
    def delete(self, request, message_id,sender_id, recipient_id):
        try:
            message = Message.objects.get(id=message_id, sender_id=sender_id, recipient_id=recipient_id)
            message.delete()
            return Response({"status": True, 'message': 'Message deleted successfully'}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"status": False, 'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)