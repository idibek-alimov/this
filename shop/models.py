from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from taggit.managers import TaggableManager
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters.html import HtmlFormatter
# from pygments import highlight


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    image = models.ImageField(upload_to='img',
                              null=True,
                              blank=True)                        

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)
class Product(models.Model):
    users_like = models.ManyToManyField(get_user_model(),
                                         #settings.AUTH_USER_MODEL,
                                         related_name='product_liked',
                                         blank=True)
    
    author = models.ForeignKey(get_user_model(),
                                 on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 related_name='category',
                                 on_delete=models.CASCADE)

    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True)
#    image = models.ImageField(upload_to='products/%Y/%m/%d',
#                              blank=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # highlighted = models.TextField() 
    tags = TaggableManager()
    
    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)
    def __str__(self):
        return self.name
    @property
    def likes_product(self):
       return self.users_like  
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id,self.slug])
# Create your models here.
    def save(self,*args,**kwargs):
        """
        Use the pygments library to create highlighted HTML
        representation of the code snippet. 
        """
                            


        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Preferences(models.Model):
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                blank=True)                                                        
    prefered_category = models.ManyToManyField(Category,
                                 related_name='prefered_category',
                                 #on_delete=models.CASCADE,
                                 blank=True)
    def __str__(self):
        return self.user.username                             
                               
