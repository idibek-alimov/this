from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#class CustomUser(AbstractUser):
 #   age = models.PositiveIntegerField(null=True,blank=True)

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    #photo = models.ImageField(upload_to='users/%Y/%m/%d/',
    #                          blank=True)

    def __str(self):
        return f'Profile for user {self.user.username}'
    def get_absolute_url(self):
        return reverse('accounts:profile',
                       args=[self.id])