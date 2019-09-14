from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from event.models import Event

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(default='default.jpg', upload_to = 'profile_pics')

    def __str__(self):
        return self.user.username + ' Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height >300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path) 