from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User

from .models import Product

class ProductTests(TestCase):

	@classmethod
	def setUpTestData(cls):
		testuser1 = User.objects.create_user(
			username='testuser1',password='abc123')
		testuser1.save()

		test_product = Product.objects.create(
			author=testuser1,name="Product",description='body contendt',category=1,price='123')
		test_post.save()

	def test_product_content(self):
	    product = Product.objects.get(id=11)
	    author = f'{post.author}'
	    	