from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    amplify_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    phonenumber = models.IntegerField(null= True , blank = True)
    is_compelet_profile = models.BooleanField(default = False)
    email = models.CharField(max_length = 300,unique=True)

    def __str__(self):
        return f' {self.email} ,{str(self.id)}'
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)




