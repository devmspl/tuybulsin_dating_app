from django.db import models
from django.conf import settings
# Create your models here.
class PersonalInformation(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('O', 'Other')
    )
    RESIDENCY_STATUS_CHOICES = (
        ('RD', 'Residency Permit'),
        ('RR', 'Residency Rule'),
        ('R', 'Resident'),
        ('O', 'Other')
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_information')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    year_of_birth = models.CharField(max_length=4)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=255)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    education = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    residency_status = models.CharField(max_length=2, choices=RESIDENCY_STATUS_CHOICES)
    religion = models.CharField(max_length=255)
    religiousness_scale = models.IntegerField()
    native_language = models.CharField(max_length=255)
    other_languages = models.CharField(max_length=255)
    other_skills = models.TextField()

    def __str__(self):
        return self.user.email
    
    
class ImageUpload(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.personal_info.user.first_name + " - " + str(self.id)