from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from user_management.models import CustomUser
from .models import ImageUpload, PersonalInformation, Plan
from .serializers import ImageUploadSerializer, PersonalInformationSerializer, PlanSerializer
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


class ProfileRetrieveAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the profile')
        ],
        responses={
            200: PersonalInformationSerializer(),
            404: "Profile not found"
        }
    )

    def get(self, request, pk):
        print('profile_id',pk)
        # profile_id = request.query_params.get('id')
        # if not profile_id:
        #     return Response({'message': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            user = CustomUser.objects.get(id=pk)
            print('user',user)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            # profile = get_object_or_404(PersonalInformation,user=user)
            profile = PersonalInformation.objects.get(user_id=user.id)
            print('profile', profile)
        except PersonalInformation.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalInformationSerializer(profile)
        return Response({'profile':serializer.data}, status=status.HTTP_200_OK)
    


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
    

class PersonalInformationFilterAPIView(APIView):
    serializer_class = PersonalInformationSerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('age', openapi.IN_QUERY, description='Filter by age', type=openapi.TYPE_INTEGER),
            openapi.Parameter('location', openapi.IN_QUERY, description='Filter by location', type=openapi.TYPE_STRING),
            openapi.Parameter('education', openapi.IN_QUERY, description='Filter by education', type=openapi.TYPE_STRING),
            openapi.Parameter('profession', openapi.IN_QUERY, description='Filter by profession', type=openapi.TYPE_STRING),
            openapi.Parameter('height', openapi.IN_QUERY, description='Filter by height', type=openapi.TYPE_STRING),
            openapi.Parameter('weight', openapi.IN_QUERY, description='Filter by weight', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        queryset = PersonalInformation.objects.all()
        age = request.query_params.get('age')
        location = request.query_params.get('location')
        education = request.query_params.get('education')
        profession = request.query_params.get('profession')
        height = request.query_params.get('height')
        weight = request.query_params.get('weight')

        if age:
            birth_year = 2024 - int(age)  # Assuming current year is 2024
            queryset = queryset.filter(year_of_birth=birth_year)
        if location:
            queryset = queryset.filter(city__icontains=location) | queryset.filter(country__icontains=location)
        if education:
            queryset = queryset.filter(education__icontains=education)
        if profession:
            queryset = queryset.filter(job_title__icontains=profession) | queryset.filter(company_name__icontains=profession)
        if height:
            queryset = queryset.filter(height=height)
        if weight:
            queryset = queryset.filter(weight=weight)

        serializer = PersonalInformationSerializer(queryset, many=True)
        return Response(serializer.data)
    

# class PlanAPIView(APIView):
#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             profile = PersonalInformation.objects.get(user=user)
#             serializer = PlanSerializer(profile.plan)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

#     def put(self, request):
#         user = request.user
#         if user.is_authenticated:
#             profile = PersonalInformation.objects.get(user=user)
#             plan_name = request.data.get('plan')
#             try:
#                 new_plan = Plan.objects.get(name=plan_name)
#                 profile.plan = new_plan
#                 profile.save()
#                 serializer = PlanSerializer(profile.plan)
#                 return Response(serializer.data)
#             except Plan.DoesNotExist:
#                 return Response({'error': 'Invalid plan'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

#     def delete(self, request):
#         user = request.user
#         if user.is_authenticated:
#             profile = PersonalInformation.objects.get(user=user)
#             default_plan = Plan.objects.get(name='basic')
#             profile.plan = default_plan
#             profile.save()
#             serializer = PlanSerializer(profile.plan)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
class PlanAPIView(APIView):
    @swagger_auto_schema(
        responses={200: PlanSerializer()},
        operation_summary="Get user's plan",
        operation_description="Get the current plan of the specified user."
    )
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(PersonalInformation, user=user)
        serializer = PlanSerializer(profile.plan)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'plan': openapi.Schema(type=openapi.TYPE_STRING, enum=['basic', 'premium'])
            },
            required=['plan']
        ),
        responses={200: PlanSerializer()},
        operation_summary="Update user's plan",
        operation_description="Update the plan of the specified user."
    )
    def put(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(PersonalInformation, user=user)
        plan_name = request.data.get('plan')
        try:
            new_plan = Plan.objects.get(name=plan_name)
            profile.plan = new_plan
            profile.save()
            serializer = PlanSerializer(profile.plan)
            return Response(serializer.data)
        except Plan.DoesNotExist:
            return Response({'error': 'Invalid plan'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: PlanSerializer()},
        operation_summary="Delete user's plan",
        operation_description="Delete the plan of the specified user, reverting to the default 'basic' plan."
    )
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(PersonalInformation, user=user)
        default_plan = Plan.objects.get(name='basic')
        profile.plan = default_plan
        profile.save()
        serializer = PlanSerializer(profile.plan)
        return Response(serializer.data)