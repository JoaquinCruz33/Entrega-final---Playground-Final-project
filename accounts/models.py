
from django.db import models
from django.contrib.auth.models import User
from PIL import Image 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'


