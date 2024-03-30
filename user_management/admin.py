from django.contrib import admin
from .models import CustomUser, OnlineUser
admin.site.register(CustomUser)
admin.site.register(OnlineUser)
# Register your models here.
