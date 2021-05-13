from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics,permissions,viewsets
from shop.models import Product ,Category,Preferences
from .serializers import ProductSerializer ,CategorySerializer,UserSerializer,PreferencesSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import filters
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from accounts.models import Profile

# class Cart(generics.ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()


class CartView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    #def get(self,request,*args,**kwargs): #or def list()
       # data = request.GET.get('params')
      #  queryset = Product.objects.filter(id__in=data)
     #   serializer = ProductSerializer(queryset, many=True)
    #    return Response(serializer.data)
    def get_queryset(self,*args,**kwargs):
        #cart = self.request.query_params['cart']
        cart = self.kwargs['cart']
        print(self.request.__dict__)
        #cart = self.request.GET.get('cart')
        
        #print(cart)
        #cart = data
        #return Product.objects.all()
        if cart:
            #return cart
            return Product.objects.filter(id__in=cart)
        return Product.objects.all()
    # def list(self, request):
    #     queryset = Product.objects.all()
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     queryset = Product.objects.all()
    #     #user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(queryset,many=True)
    #     return Response(serializer.data)    
    


class SimilarTagsProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self,*args,**kwargs):
        product = get_object_or_404(Product,pk=self.kwargs['pk'])
        product_tags_ids = product.tags.values_list('id',flat=True)
        similar_products = Product.objects.filter(tags__in=product_tags_ids)\
                                          .exclude(id=product.id)
      							  
        return  Product.objects.filter(tags__in=product_tags_ids).exclude(id=product.id)


class CategoryProductFilter(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self,*args,**kwargs):
        search_vector = SearchVector('name','description')
        search_query = SearchQuery(self.kwargs['search'])
        

        if self.kwargs['search'] == 'und':
            return Product.objects.filter(category__id=self.kwargs['category'])
        elif self.kwargs['category'] == 0 :
            return Product.objects.annotate(
            similarity = TrigramSimilarity('name',self.kwargs['search']),
            ).filter(similarity__gt=0.1).order_by('-similarity')
        
        else :
            return Product.objects.annotate(
            similarity = TrigramSimilarity('name',self.kwargs['search']),
            ).filter(similarity__gt=0.1,category__id=self.kwargs['category']).order_by('-similarity')

        



class ProductByCategoryListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__id']


@api_view(['POST'])
def product_create(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)	

@api_view(['POST'])
def preference_create(request):
    if request.method == 'POST':
        serializer = PreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)	







class LikedProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(users_like = user)


        


class Profile(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(author = user) 
    



class ProductViewSet(viewsets.ModelViewSet): # new
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer	
  
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer		
    
class PreferencesViewSet(viewsets.ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
    def get_queryset(self,*args,**kwargs):
        #product = get_object_or_404(Preferences,user=self.request.user)
        product = Preferences.objects.filter(user=self.request.user)
        return product


        


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer 	


def product_search():
  query = 'qrbon'
  search_vector = SearchVector('name','description',)
  search_query = SearchQuery(query)
  return Product.objects.annotate(similarity=TrigramSimilarity('name',query),).filter(similarity__gt=0.1).order_by('-similarity')
     


class SearchListView(generics.ListAPIView):
    queryset = product_search()
    serializer_class = ProductSerializer

from .serializers import ProfileSerializer
class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    

# class CreateProduct(generics.ListCreateAPIView):
#  	permission_classes = (permissions.IsAuthenticated,)
#     #queryset = Product.objects.all()
#  	serializer_class = ProductSerializer
#     def perform_create(self,serializer):
#         serializer.save(author = self.request.user)
       

# class ListAPIView(generics.ListCreateAPIView):
# 	#permission_classes = (permissions.IsAuthenticated,)
# 	#permission_classes = (IsAuthorOrReadOnly,)
# 	queryset = Product.objects.all()
# 	serializer_class = ProductSerializer


# class CategoryListView(generics.ListAPIView):
# 	queryset = Category.objects.all()
# 	serializer_class = CategorySerializer

# class UserList(generics.ListCreateAPIView):
# 	queryset = get_user_model().objects.all()
# 	serializer_class = UserSerializer


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = get_user_model().objects.all()
# 	serializer_class = UserSerializer
