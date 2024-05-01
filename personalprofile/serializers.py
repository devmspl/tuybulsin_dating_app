import uuid
from rest_framework import serializers

from user_management.models import CustomUser
from user_management.serializers import CustomUserSerializer

from .models import PersonalInformation, Plan, UserPreference
from rest_framework.validators import UniqueValidator

from .models import ImageUpload
import boto3
from botocore.exceptions import ClientError

class PersonalInformationSerializer(serializers.ModelSerializer):
   
    images = serializers.SerializerMethodField()
    preference = serializers.SerializerMethodField()
   
    def get_preference(self, obj):
        try:
            custom_user = obj.user
            user_preferences = custom_user.user_preference.all()
            preferences = []
            for user_preference in user_preferences:
                preferences.append({
                    'age_min': user_preference.age_min,
                    'age_max': user_preference.age_max,
                    'location': user_preference.location,
                    'education': user_preference.education,
                    'profession': user_preference.profession,
                    'height': user_preference.height,
                    'weight': user_preference.weight,
                })
            return preferences
        except UserPreference.DoesNotExist:
            return None
            # user_preference = obj.user_preference.all()
        #     return {
        #         'age_min': user_preference.age_min,
        #         'age_max': user_preference.age_max,
        #         'location': user_preference.location,
        #         'education': user_preference.education,
        #         'profession': user_preference.profession,
        #         'height': user_preference.height,
        #         'weight': user_preference.weight,
        #     }
        # except UserPreference.DoesNotExist:
        #     return None
    
    class Meta:
        model = PersonalInformation
        fields = ('id', 'first_name', 'last_name', 'location', 'gender', 'year_of_birth', 'marital_status', 'nationality', 'height', 'weight', 'education', 'job_title', 'company_name', 'city', 'country', 'residency_status', 'religion', 'religiousness_scale', 'native_language', 'other_languages', 'other_skills', 'smoking', 'drinking', 'phone_number', 'user', 'plan', 'images','preference','contact_person_first_name','contact_person_last_name','contact_relationship_sibs')

  
    def get_images(self, obj):
        image_uploads = ImageUpload.objects.filter(personal_info=obj)
        return [upload.image.url for upload in image_uploads]


class ImageUploadSerializer(serializers.Serializer):
    # image = serializers.ImageField()
    
    # class Meta:
    #     model = ImageUpload
    #     fields = ('image_url', 'uploaded_at', 'personal_info')

    # def get_image_url(self, obj):
    #     s3_client = boto3.client('s3')
    #     try:
    
    #         # Generate a pre-signed URL for the image
    #         url = s3_client.generate_presigned_url(
    #             'get_object',
    #             Params={'Bucket': 'dating-static-jar', 'Key': obj.image_key},
    #             ExpiresIn=3600  # URL expires in 1 hour (3600 seconds)
    #         )
    #     except ClientError as e:
    #         url = None
    #         # Handle any errors that occur
    #         print(e)
    #     return url
    images = serializers.ListField(child=serializers.ImageField())

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        image_urls = []
        s3_bucket = 'dating-static-jar'
        s3_client = boto3.client('s3')

        for image_data in images_data:
            # Generate a unique key for each image
            image_key = 'images/' + str(uuid.uuid4()) + '/' + image_data.name
            try:
                # Upload the image to S3
                s3_client.upload_fileobj(image_data, s3_bucket, image_key)
                # Generate a pre-signed URL for the uploaded image
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': s3_bucket, 'Key': image_key},
                    ExpiresIn=3600  # URL expires in 1 hour (3600 seconds)
                )
                image_urls.append(url)
            except ClientError as e:
                # Handle any errors that occur during upload
                print(e)
        return {'image_urls': image_urls}

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan

        fields = '__all__'


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'