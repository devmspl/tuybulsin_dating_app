from rest_framework import serializers

from user_management.models import CustomUser
from user_management.serializers import CustomUserSerializer

from .models import PersonalInformation, Plan, UserPreference
from rest_framework.validators import UniqueValidator



class PersonalInformationSerializer(serializers.ModelSerializer):
    # profile = serializers.CharField(source='user_id')
    # user_id = serializers.PrimaryKeyRelatedField(
    #     source='user',  # Use 'custom_user' field from PersonalInformation model
    #     queryset=CustomUser.objects.all(),
    #     validators=[UniqueValidator(queryset=PersonalInformation.objects.all())]
    # )
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