from django.contrib import admin
from .models import PersonalInformation, ImageUpload, Plan, UserPreference, AudioMessage
# Register your models here.
admin.site.register(PersonalInformation)
admin.site.register(ImageUpload)
admin.site.register(Plan)
admin.site.register(UserPreference)
admin.site.register(AudioMessage)