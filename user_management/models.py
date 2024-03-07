from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    # email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    phonenumber = models.IntegerField(null= True , blank = True)
    is_compelet_profile = models.BooleanField(default = False)

    def __str__(self):
        return f' {self.first_name} ,{str(self.id)}'
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.first_name
        super().save(*args, **kwargs)

