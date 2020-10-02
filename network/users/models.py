from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('self', related_name='followers',symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username 