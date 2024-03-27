from user_management.models import CustomUser
from rest_framework import serializers

from .models import  Message
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
      


# class ConversationListSerializer(serializers.ModelSerializer):
  

#     initiator = UserSerializer()
#     receiver = UserSerializer()

#     last_message = serializers.SerializerMethodField()

#     class Meta:

#         model = Conversation
#         fields = ['initiator', 'receiver', 'last_message']




#     def get_last_message(self, instance):
#         message = instance.message_set.first()
#         return MessageSerializer(instance=message)



