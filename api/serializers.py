from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from shop.models import Product,Category,Preferences
from accounts.models import Profile
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')
    #liked_product = serializer.ReadOnlyField(source=liked_product)
	def get_like(self,obj):
		
		#user =  self.context['request'].user
		request = self.context.get("request")
		user = request.user
		#return user.username
		if user in obj.users_like.all():
			return 1
		else:
			return 0	
	likes_product = serializers.SerializerMethodField('get_like')	
	class Meta:
		model = Product
		fields = ('category','id','name','price','image','description','author','likes_product')

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('name','id','image')

class PreferencesSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	class Meta:
		model = Preferences
		fields = ('id','user','prefered_category',)


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('__all__')		

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id','username',)

