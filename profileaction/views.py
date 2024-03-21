import random
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from personalprofile.serializers import PersonalInformationSerializer
# Create your views here.
from .models import PersonalInformation, LikeDislike
from .serializers import LikeDislikeSerializer
from user_management.models import CustomUser
from django.core import serializers



class LikeProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, pk, format=None):
        profile = PersonalInformation.objects.get(pk=pk)
        like, created = LikeDislike.objects.get_or_create(user=request.user, profile=profile)
        if not created:
            like.liked = True
            like.save()
        return Response({"message": "Profile liked successfully."}, status=200)


class LikedProfileByUserId(APIView):
    def get(self, request, user_id):
        likes = LikeDislike.objects.filter(user_id=user_id, liked=True)
        serializer = LikeDislikeSerializer(likes, many=True)
        # print(serializer.data)
        profiles = [item['profile'] for item in serializer.data]
        profile_dict = {}
        lst = []
        for id in profiles:
            user_profiles = PersonalInformation.objects.filter(id = id)
            # print('v',user_profiles.values())
            
            for profile in user_profiles.values():
                print('profile',profile)
            lst.append(profile)
       

        print('profile-liked',PersonalInformation.objects.get(id = id))
        return Response({'message':'liked profiles get successfully','data':lst,'success_status':'true'},status=200)
    

class LikedProfileByProfileId(APIView):
    def get(self, request, profile_id):
        likes = LikeDislike.objects.filter(profile_id=profile_id, liked=True)
        serializer = LikeDislikeSerializer(likes, many=True)
        return Response(serializer.data)



class DislikeProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, pk, format=None):
        profile = PersonalInformation.objects.get(pk=pk)
        LikeDislike.objects.filter(user=request.user, profile=profile).delete()
        return Response({"message": "Profile disliked successfully."}, status=200)


class LikedProfilesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
 


    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):


        assert request.user.is_authenticated, "User must be authenticated"
        print('profile', request.user)
        
        # Assuming CustomUser model is imported correctly
        user = CustomUser.objects.filter(id=request.user.id).first()
        print('custom user', user)

        liked_profiles = PersonalInformation.objects.filter(likedislike__user=user, likedislike__liked=True)
        print('liked', liked_profiles)

        serializer = PersonalInformationSerializer(liked_profiles, many=True)
        return Response(serializer.data, status=200)
    

class RandomProfileView(APIView):
    authentication_classes = [TokenAuthentication]
 
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profiles = PersonalInformation.objects.all()
        if profiles.exists():
            profile = random.choice(profiles)
            serializer = PersonalInformationSerializer(profile)
            return Response({'message':'profile selected','data':serializer.data,'success_status':'true'})
        else:
            return Response({"message": "No profiles available",'success_status':'false'}, status=404)