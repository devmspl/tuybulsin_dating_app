from django.db import models
from django.conf import settings

from user_management.models import CustomUser
# Create your models here.


class Plan(models.Model):
    BASIC = 'basic'
    PREMIUM = 'premium'
    PLAN_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, default=BASIC)
    features1 = models.TextField()
    features2 = models.TextField()
    features3 = models.TextField()


    def __str__(self):
        return self.get_name_display()

class PersonalInformation(models.Model):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # 
    #     ('O', 'Other')
    # )
    # MARITAL_STATUS_CHOICES = (
    #     ('S', 'Single'),
    #     ('M', 'Married'),
    #     ('D', 'Divorced'),
    #     ('W', 'Widowed'),
    #     ('O', 'Other')
    # )
    # RESIDENCY_STATUS_CHOICES = (

    #     ('RD', 'Residency Permit'),
    #     ('RR', 'Residency Rule'),
    #     ('R', 'Resident'),
    #     ('O', 'Other')
    # )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_information')
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length = 200,blank=True,null=True)
    last_name = models.CharField(max_length = 200,blank=True,null=True)
    location = models.CharField(max_length = 200,blank=True,null=True)
    gender = models.CharField(max_length=100)
    year_of_birth = models.CharField(max_length=50,default=0)
    # marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    marital_status = models.CharField(max_length=100)
    nationality = models.CharField(max_length=255)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    education = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    # residency_status = models.CharField(max_length=2, choices=RESIDENCY_STATUS_CHOICES)
    residency_status = models.CharField(max_length=200)
    religion = models.CharField(max_length=255)
    religiousness_scale = models.IntegerField()
    native_language = models.CharField(max_length=255)
    other_languages = models.CharField(max_length=255)
    other_skills = models.TextField()
    # plan = models.ForeignKey(Plan, on_delete=models.SET_DEFAULT, default=Plan.objects.get(name='basic'))
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_id
    
    
class ImageUpload(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.personal_info.user.first_name + " - " + str(self.id)
    

class UserPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age_min = models.IntegerField(blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email