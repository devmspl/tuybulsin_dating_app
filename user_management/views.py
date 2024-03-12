from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.parsers import FileUploadParser




class SignupSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    amplify_user_id = serializers.CharField(max_length = 500)
    phonenumber = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    #image = serializers.ImageField()
    #is_compelet_profile = serializers.BooleanField(default = False)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return CustomUser.objects.create(**validated_data)
   



class UserSignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
      
        manual_parameters=[
            # openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            # openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, required=True),
            openapi.Parameter('amplify_user_id', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('phonenumber', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, required=True),
            #openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
        ],
        responses={
            201: 'Created',
            400: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amplify_user_id = request.data.get('amplify_user_id')
            # Process the valid data
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            phonenumber = serializer.validated_data.get('phonenumber')
            password = serializer.validated_data.get('password')
            
            #image = serializer.validated_data.get('image')
            serializer.save()
            # Your signup logic here

            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(ObtainAuthToken):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'amplify_user_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['amplify_user_id']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description='Login successful'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(description='Login failed'),
            status.HTTP_404_NOT_FOUND: openapi.Response(description='User does not exist'),
        }
    )
    def post(self, request):
        amplify_user_id = request.data.get('amplify_user_id')
        email = request.data.get('email')
        # Check if a user with the given amplify_user_id exists
        try:
            user = CustomUser.objects.get(amplify_user_id=amplify_user_id)
             
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(amplify_user_id=amplify_user_id,email = email)
           
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Authenticate the user
        # user = authenticate(request, username=user.amplify_user_id, password=None)
        if user is not None:
            login(request, user)
          
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful','token': token.key},status=status.HTTP_200_OK)
        else:
             
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
       

class UserLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['amplify_user_id'],
            properties={
                # 'phonenumber': openapi.Schema(type=openapi.TYPE_NUMBER),
                # 'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'amplify_user_id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description='Token is generated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        # phonenumber = request.data.get('phonenumber')
        # password = request.data.get('password')
        amplify_user_id = request.data.get('amplify_user_id')
        email = request.data.get('email')
        if not amplify_user_id :
            return Response({'error': 'Please provide amplify_user_id'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(amplify_user_id=amplify_user_id).first()
        print(user,user.username)
        # if not user or not user.check_password(password):
        #     return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        # return super().post(request, *args, **kwargs)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    


    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Token is retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: 'Unauthorized',
        }
    )
    def get(self, request, *args, **kwargs):
        # Ensure user is authenticated
        if request.user.is_authenticated:
            token, _ = Token.objects.get_or_create(user=request.user)
            return Response({'token': token.key,'username': request.user.username})
        else:
            return Response(status=401)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
   
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='User ID',
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User details retrieved successfully',
                schema=SignupSerializer,
            ),
            401: 'Unauthorized',
        }
    )
    def get(self, request, id):
        user = get_object_or_404(CustomUser, pk=id)
        serializer = SignupSerializer(user)
        return Response(serializer.data)
    
class ImageUploadField(serializers.FileField):
    def to_internal_value(self, data):
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    image = ImageUploadField(required=False)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'image']

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='User ID',
                required=True,
            ),
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ],
      
        responses={
            200: 'Updated successfully',
            400: 'Bad Request',
        }
    )
    def put(self, request, id):
        user = get_object_or_404(CustomUser, pk=id)
        print('update user',user)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated successfully")
        return Response(serializer.errors, status=400)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='User ID',
                required=True,
            ),
        ],
        responses={
            204: 'Deleted successfully',
            401: 'Unauthorized',
        }
    )
    def delete(self, request, id):
        user = get_object_or_404(CustomUser, pk=id)
        user.delete()
        return Response("Deleted successfully", status=204)
