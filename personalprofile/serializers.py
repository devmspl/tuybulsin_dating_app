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
    # first_name = serializers.CharField(source='user.first_name', read_only=True)
    # last_name = serializers.CharField(source='user.last_name', read_only=True)
    # phone_number = serializers.IntegerField(source='user.phonenumber', read_only=True)
    # profile = serializers.CharField(source='user_id')
    # user_id = serializers.PrimaryKeyRelatedField(
    #     source='user',  # Use 'custom_user' field from PersonalInformation model
    #     queryset=CustomUser.objects.all(),
    #     validators=[UniqueValidator(queryset=PersonalInformation.objects.all())]
    # )
    images = serializers.ImageField(source='images.first().image', read_only=True)
    
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