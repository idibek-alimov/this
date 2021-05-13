from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from shop.models import Category
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    
    preferences = models.ManyToManyField(Category,
                                related_name='category_pref',
    )#                                 on_delete=models.CASCADE) 

    def __str__(self):
        return f'Profile for user {self.user.username}'
    def get_absolute_url(self):
        return reverse('accounts:profile',
                       args=[self.id])