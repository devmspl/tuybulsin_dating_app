from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import ImageUpload, PersonalInformation
from .serializers import ImageUploadSerializer, PersonalInformationSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PersonalInformation
from .serializers import PersonalInformationSerializer

class ProfileCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PersonalInformationSerializer,
        responses={200: PersonalInformationSerializer()},
    )

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # Set the user field based on the authenticated user
        serializer = PersonalInformationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                'year_of_birth': openapi.Schema(type=openapi.TYPE_STRING),
                'marital_status': openapi.Schema(type=openapi.TYPE_STRING),
                'nationality': openapi.Schema(type=openapi.TYPE_STRING),
                'height': openapi.Schema(type=openapi.TYPE_STRING),
                'weight': openapi.Schema(type=openapi.TYPE_STRING),
                'education': openapi.Schema(type=openapi.TYPE_STRING),
                'job_title': openapi.Schema(type=openapi.TYPE_STRING),
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'city': openapi.Schema(type=openapi.TYPE_STRING),
                'country': openapi.Schema(type=openapi.TYPE_STRING),
                'residency_status': openapi.Schema(type=openapi.TYPE_STRING),
                'religion': openapi.Schema(type=openapi.TYPE_STRING),
                'religiousness_scale': openapi.Schema(type=openapi.TYPE_INTEGER),
                'native_language': openapi.Schema(type=openapi.TYPE_STRING),
                'other_languages': openapi.Schema(type=openapi.TYPE_STRING),
                'other_skills': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['gender', 'year_of_birth', 'marital_status', 'nationality', 'height', 'weight', 'education', 'job_title', 'company_name', 'city', 'country', 'residency_status', 'religion', 'religiousness_scale', 'native_language', 'other_languages', 'other_skills'],
        ),
        responses={
            '200': openapi.Response('OK', PersonalInformationSerializer),
            '400': 'Bad Request',
        },
        operation_id='updateProfile'
    )
    def put(self, request, *args, **kwargs):
        # Exclude 'user' field from request data
        request_data = request.data.copy()
        request_data.pop('user', None)

        # Get the profile instance
        try:
            profile = request.user.personal_information
        except PersonalInformation.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Update the profile
        serializer = PersonalInformationSerializer(profile, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUploadAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ],
        responses={
            '200': openapi.Response('OK'),
            '400': 'Bad Request',
        },
        operation_id='uploadImage'
    )
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            # Get the PersonalInformation instance associated with the authenticated user
            personal_info = PersonalInformation.objects.get(user=request.user)
            ImageUpload.objects.create(personal_info=personal_info, image=image)
            return Response({"message": "Image uploaded successfully."}, status=200)
        return Response(serializer.errors, status=400)