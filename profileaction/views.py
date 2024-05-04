from math import atan2, cos, radians, sin, sqrt
import random
import re
from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from personalprofile.models import UserPreference
from personalprofile.serializers import PersonalInformationSerializer, UserPreferenceSerializer
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
        if profile.user == request.user:
            return Response({"message": "You cannot like your own profile."}, status=400)
        
        like, created = LikeDislike.objects.get_or_create(user=request.user, profile=profile)
        if not created:
            if not like.liked:  # Check if the user hasn't already liked the profile
                like.liked = True
                like.save()
                return Response({"message": "Profile liked successfully."}, status=200)
            else:
                return Response({"message": "You have already liked this profile."}, status=400)
        return Response({"message": "Profile liked successfully."}, status=200)


class LikedProfileByUserId(APIView):
    def get(self, request, user_id):
        likes = LikeDislike.objects.filter(user_id=user_id, liked=True)
        serializer = LikeDislikeSerializer(likes, many=True)
        print(serializer.data)
        profiles = [item['profile'] for item in serializer.data]
        profile_dict = {}
        lst = []
        for id in profiles:
            user_profiles = PersonalInformation.objects.filter(id = id)
            serializer = PersonalInformationSerializer(user_profiles[0])
            profile_data = serializer.data
            profile_data['images'] = serializer.get_images(user_profiles[0])
            # print('image',profile_data)
            # print('v',user_profiles.values())
            
            for profile in user_profiles:
                print('profile',profile)
                user_profile = PersonalInformation.objects.filter(id=profile.id).first()
                serializer = PersonalInformationSerializer(user_profile)
                profile_instance = user_profile.user
                amplify_user_id = profile_instance.amplify_user_id
                profile_data = serializer.data
                profile_data['images'] = serializer.get_images(profile)
                profile_data['amplify_user_id'] = amplify_user_id
                print('profile',profile_data)
                lst.append(profile_data)
       

        # print('profile-liked',PersonalInformation.objects.get(id = id))
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

# def customfilter(location,education,profession,height,weight,age_min,age_max):


# def convert_to_decimal(coord):
#     parts = re.split('[°\'"]', coord)
#     if len(parts) == 2:
#         degrees, direction = parts
#         return float(degrees) if direction.strip() in ['N', 'E'] else -float(degrees)
#     elif len(parts) == 4:
#         degrees, minutes, direction = parts[:3]
#         return float(degrees) + float(minutes) / 60 if direction.strip() in ['N', 'E'] else -(float(degrees) + float(minutes) / 60)
#     elif len(parts) == 6:
#         degrees, minutes, seconds, direction = parts[:4]
#         return float(degrees) + float(minutes) / 60 + float(seconds) / 3600 if direction.strip() in ['N', 'E'] else -(float(degrees) + float(minutes) / 60 + float(seconds) / 3600)
#     else:
#         raise ValueError("Invalid coordinate format")

def convert_to_decimal(coord):
    if coord is None:
        return 0.0
    return float(coord)


class RandomProfileView(APIView):
    authentication_classes = [TokenAuthentication]
 
    permission_classes = [IsAuthenticated]


    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # approximate radius of Earth in km

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    def get(self, request):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user_preference = UserPreference.objects.get(user_id = user_id)
        user_prefernce_serializer = UserPreferenceSerializer(user_preference)

        lat1 = float(convert_to_decimal(user_prefernce_serializer.data['lat']))
        lon1 = float(convert_to_decimal(user_prefernce_serializer.data['long']))
        distance = float(user_prefernce_serializer.data['distance'])
       
        print("userprefernce", user_prefernce_serializer.data)
        # distance = user_prefernce_serializer.data['distance']
        education = user_prefernce_serializer.data['education']
        profession = user_prefernce_serializer.data['profession']
        height = user_prefernce_serializer.data['height']
        weight = user_prefernce_serializer.data['weight']
        age_min = user_prefernce_serializer.data['age_min']
        age_max = user_prefernce_serializer.data['age_max']
        # lat = user_prefernce_serializer.data['lat']
        # long = user_prefernce_serializer.data['long']
        print("location",distance)

 
        filters =  Q()
  
        if education:
                filters |= Q(user_preference__education=education)

        if profession:
                filters |= Q(user_preference__profession=profession)
        if height:
                filters |= Q(user_preference__height=height)
        if weight:
                filters |= Q(user_preference__weight=weight)
        if age_min:
                filters |= Q(user_preference__age_min=age_min)
        if age_max:
                filters |= Q(user_preference__age_max=age_max)
        
        # filter_user_by_prefernce = CustomUser.objects.filter(userpreference__location=location,userpreference__education = education,userpreference__profession = profession, userpreference__height = height , userpreference__weight = weight , userpreference__age_min = age_min , userpreference__max = age_max)
        filter_user_by_prefernce = CustomUser.objects.filter(filters).exclude(id=user.id)

        # print('filter user', filter_user_by_prefernce)
        profiles = PersonalInformation.objects.filter(user__in=filter_user_by_prefernce)
        serialized_profiles = PersonalInformationSerializer(instance=profiles, many=True)
        # serialized_profiles['preference'] =  
        # print("serialized_profiles",serialized_profiles.data)

        if distance > 0:
            print('distance',distance)
            nearby_users = []
            for other_user in filter_user_by_prefernce:
                user_preference = other_user.user_preference.get()
                lat2 = float(convert_to_decimal(user_preference.lat))
                lon2 = float(convert_to_decimal(user_preference.long))
                print('lat2',lat2,lon2)
                other_user_distance = self.haversine_distance(lat1, lon1, lat2, lon2)
                print('other user distance',other_user_distance)
                if other_user_distance <= distance:
                    profiles = PersonalInformation.objects.filter(user=other_user)
                    profile = random.choice(profiles)
                    serializer = PersonalInformationSerializer(profile)
                    profile_instance = profile.user
                    amplify_user_id = profile_instance.amplify_user_id
                    profile_data = serializer.data
                    profile_data['images'] = serializer.get_images(profile)
                    profile_data['amplify_user_id'] = amplify_user_id
                    nearby_users.append(other_user)

                filter_user_by_preference = nearby_users

                print('filter user', filter_user_by_preference)
                return Response({'message':'profile selected','data': profile_data,'success_status':'true'})
              

        profiles = PersonalInformation.objects.filter()
        if profiles.exists():
            profile = random.choice(profiles)
            profile_instance = profile.user
            amplify_user_id = profile_instance.amplify_user_id
            serializer = PersonalInformationSerializer(profile)
            profile_data = serializer.data
            profile_data['images'] = serializer.get_images(profile)
            profile_data['amplify_user_id'] = amplify_user_id
            return Response({'message':'profile selected','data': profile_data,'success_status':'true'})
        else:
            return Response({"message": "No profiles available",'success_status':'false'}, status=404)