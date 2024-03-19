from rest_framework import serializers

from user_management.models import CustomUser
from user_management.serializers import CustomUserSerializer

from .models import PersonalInformation, Plan, UserPreference
from rest_framework.validators import UniqueValidator



class PersonalInformationSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    # phone_number = serializers.IntegerField(source='user.phonenumber', read_only=True)
    # profile = serializers.CharField(source='user_id')
    # user_id = serializers.PrimaryKeyRelatedField(
    #     source='user',  # Use 'custom_user' field from PersonalInformation model
    #     queryset=CustomUser.objects.all(),
    #     validators=[UniqueValidator(queryset=PersonalInformation.objects.all())]
    # )
    class Meta:
        model = PersonalInformation
        fields = '__all__'

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     profile_data = {
    #         'user': user,
    #         'first_name': user.first_name,
    #         'last_name': user.last_name,
    #         'phone_number': user.phonenumber,
    #         **validated_data
    #     }
    #     profile = PersonalInformation.objects.create(**profile_data)
    #     return profile


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