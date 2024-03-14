from rest_framework import serializers
from .models import PersonalInformation, Plan

class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'