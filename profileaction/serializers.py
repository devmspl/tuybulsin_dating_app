from rest_framework import serializers

from personalprofile.serializers import PersonalInformationSerializer
from .models import LikeDislike

class LikeDislikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LikeDislike
        fields = '__all__'

    def get_profile(self, obj):
        return PersonalInformationSerializer(obj.profile).data