from rest_framework import serializers

from user_management.models import CustomUser
from user_management.serializers import CustomUserSerializer

from .models import PersonalInformation, Plan, UserPreference


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['username', 'email','last_login','is_superuser','password','is_staff','is_active','date_joined','amplify_user_id','phonenumber','groups','user_permissions']

class PersonalInformationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = PersonalInformation
        fields = '__all__'


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'