import os
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import render
import stripe
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from personalprofile.forms import UserPreferenceForm
from user_management.models import CustomUser
from .models import ImageUpload, PersonalInformation, Plan, UserPreference
from .serializers import ImageUploadSerializer, PersonalInformationSerializer, PlanSerializer, UserPreferenceSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PersonalInformation
from .serializers import PersonalInformationSerializer
from .models import ImageUpload
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage
from urllib.parse import urlparse




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
            return Response({'message':'profile created successfully!!!','data':serializer.data,'success_status':'true'}, status=status.HTTP_201_CREATED)
        return Response({'meaasge':serializer.errors,'success_status':'false'},status=status.HTTP_400_BAD_REQUEST)


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
            error_data = {'message': 'profile not found','success_status':'false'}
            return Response({'message': 'profile not found','success_status':'false'}, status=status.HTTP_404_NOT_FOUND)
        try:
            # profile = get_object_or_404(PersonalInformation,user=user)
            profile = PersonalInformation.objects.get(user_id=user.id)
            
            # print('profile', profile)
        except PersonalInformation.DoesNotExist:
           
            return Response({'message': 'profile not found','success_status':'false'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalInformationSerializer(profile)
        print(serializer.data)
        data = serializer.data
        data['image'] = profile.images.first().image.url if profile.images.first() else None
        
        return Response({'message':'profile retrieve successfully','data':data,'success_status':'true'}, status=status.HTTP_200_OK)
    


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
            #required=['gender', 'year_of_birth', 'marital_status', 'nationality', 'height', 'weight', 'education', 'job_title', 'company_name', 'city', 'country', 'residency_status', 'religion', 'religiousness_scale', 'native_language', 'other_languages', 'other_skills'],
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
            return Response({"error": "Profile does not exist",'success_status':'false'}, status=status.HTTP_404_NOT_FOUND)

        # Update the profile
        serializer = PersonalInformationSerializer(profile, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'profile updated successfully!!!','data':serializer.data,'success_status':'true'}, status=status.HTTP_200_OK)
        return Response({'message':'an error occurred', 'error':serializer.errors,'success_status':'false'}, status=status.HTTP_400_BAD_REQUEST)


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
            if settings.USE_S3:
                user = request.user
                print(user.id)
                personal_info = PersonalInformation.objects.get(user=user.id)
                image_files = request.FILES.getlist('image')
                image_urls = []
                for image_file in image_files:
                    upload = ImageUpload(personal_info=personal_info,image=image_file)
                    upload.save()
                    image_urls.append(upload.image.url)
                print('image_url',image_urls)
                return Response({"message": "Image uploaded successfully.",'data':image_urls,'success_status':'true'}, status=200)
            else:

                serializer = ImageUploadSerializer(data=request.data)
                if serializer.is_valid():
                    image = serializer.validated_data['image']
                    # Get the PersonalInformation instance associated with the authenticated user
                    personal_info = PersonalInformation.objects.get(user=request.user)
                    ImageUpload.objects.create(personal_info=personal_info, image=image)
                    return Response({"message": "Image uploaded successfully.",'success_status':'true'}, status=200)
            return Response(serializer.errors, status=400)
    


import boto3

class ImageDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
       
        try:
            print("------------------------------")
            print('data',request.data)
            # Get the image URL from the request data
            s3 = default_storage
            s3.open('https://eternity-match.s3.us-east-1.amazonaws.com/media/OIG1_1.jpg', 'w')
            image_url = request.data.get('image_url')
            print('image',image_url)
            parsed_url = urlparse(image_url)
            
            image_file_name = os.path.basename(parsed_url.path)
            print('image_file_name',image_file_name)

            
            image = ImageUpload.objects.get(image__icontains=image_file_name)
            print('image',image)
            # Check if the user is the owner of the image
            if image.personal_info.user != request.user:
                return Response({"message": "You are not authorized to delete this image."}, status=status.HTTP_403_FORBIDDEN)
            # Delete the image
            image.delete()
            # Delete the image file from S3        
            if settings.USE_S3:
                storage = S3Boto3Storage()
                storage.delete(image.image.name)
                
                parsed_url = urlparse(image_url)
                print('parsed_url',parsed_url)
                storage.delete(parsed_url.path.lstrip('/'))
                return Response({"message": "Image deleted successfully.", 'success_status': 'true'}, status=status.HTTP_200_OK)
          
        except ImageUpload.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        



    


class SetUserPreferenceAPIView(APIView):
    @swagger_auto_schema(
        responses={200: UserPreferenceSerializer(many=True)}
    )
    def get(self, request, user_id):
        preferences = UserPreference.objects.filter(user_id=user_id)
        serializer = UserPreferenceSerializer(preferences, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserPreferenceSerializer,
        responses={200: UserPreferenceSerializer}
    )
    def post(self, request, user_id):
        request.data['user'] = user_id
        serializer = UserPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'prefrence is created','data':serializer.data,'success_status':'true'}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors,'success_status':'false'}, status=status.HTTP_400_BAD_REQUEST)

class UserPreferenceAPIView(APIView):
    @swagger_auto_schema(
        responses={200: UserPreferenceSerializer(many=True)}
    )
    def get(self, request, user_id):
        preferences = UserPreference.objects.filter(user_id=user_id)
        serializer = UserPreferenceSerializer(preferences, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserPreferenceSerializer,
        responses={200: UserPreferenceSerializer}
    )
    def post(self, request, user_id):
        request.data['user'] = user_id
        serializer = UserPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserPreferenceAPIView(APIView):
    @swagger_auto_schema(request_body=UserPreferenceSerializer)
    def put(self, request):
        # print('request-data',request.data)

        form = UserPreferenceForm(request.data)
        if form.is_valid():
            amplify_user_id = request.data.get('amplify_user_id')
           # amplify_user_id = form.cleaned_data.get('amplify_user_id')
            print('amplify_id',amplify_user_id)
            age_min =  request.data.get('age_min')
            age_max =  request.data.get('age_max')
            location =  request.data.get('location')
            education =  request.data.get('education')
            profession =  request.data.get('profession')
            height =  request.data.get('height')
            weight =  request.data.get('weight')
            try:
                user = CustomUser.objects.get(id=request.user.id)
                print('user',user)
                user_preference = UserPreference.objects.get(user=user)
                print('user prefernece',user_preference)
                user_preference.age_min = age_min
                user_preference.age_max = age_max
                user_preference.location = location
                user_preference.education = education
                user_preference.profession = profession
                user_preference.height = height
                user_preference.weight = weight
                user_preference.save()
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            serializer = UserPreferenceSerializer(user_preference)
            return Response(serializer.data, status=200)
        return Response(form.errors, status=400)
    
class GetUserPreferenceAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description='User ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter('amplify_user_id', openapi.IN_QUERY, description='Amplify User ID', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        amplify_user_id = request.query_params.get('amplify_user_id')

        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        elif amplify_user_id:
            try:
                user = CustomUser.objects.get(amplify_user_id=amplify_user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            return Response({"error": "Please provide user_id or amplify_user_id"}, status=400)

        try:
            user_preference = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            return Response({"error": "User preference not found"}, status=404)

        serializer = UserPreferenceSerializer(user_preference)
        return Response(serializer.data, status=200)

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
    

stripe.api_key = settings.STRIPE_SECRET_KEY

class PurchasePlanView(APIView):
    def post(self, request, user_id, plan_id):
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return JsonResponse({'error': 'Plan not found'}, status=404)

        # Create a PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=10000,  # Replace with the actual amount in cents
            currency='usd',
            payment_method_types=['card']
        )

        # Return PaymentIntent and plan information
        return JsonResponse({
            'payment_intent': payment_intent.client_secret,
            'price': plan.price,  # You need to add a price field to your Plan model
            'plan': {
                'id': plan.id,
                'name': plan.name,
                'features1': plan.features1,
                'features2': plan.features2,
                'features3': plan.features3
            }
        })

class CancelPlanView(APIView):
    def post(self, request, user_id, plan_id):
        try:
            user_plan = Plan.objects.get(user_id=user_id, plan_id=plan_id, active=True)
        except Plan.DoesNotExist:
            raise Http404('User plan not found or already canceled')

        # Update the user plan to mark it as canceled
        user_plan.active = False
        user_plan.save()

        return JsonResponse({'message': 'Plan canceled'})
    

