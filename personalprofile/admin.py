from django.contrib import admin
from .models import PersonalInformation, ImageUpload
# Register your models here.
admin.site.register(PersonalInformation)
admin.site.register(ImageUpload)