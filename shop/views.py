from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Category,Product
from django.views.generic import ListView,CreateView
from django.db.models import Q
from django.http import Http404
from cart.forms import CartAddProductForm
from django.db.models import Count
from rest_framework import status,mixins,generics,renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse 
#from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from api.serializers import ProductSerializer


from rest_framework import filters

class FilterListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']



@api_view(['GET'])
def search_by_url_text(query):
    search_vector = SearchVector('name','description')
    search_query = SearchQuery(query)
    products  = Product.objects.annotate(
        similarity=TrigramSimilarity('name',query),
        ).filter(similarity__gt=0.1).order_by('-similarity')
   
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)




@api_view(['GET'])
def product_filter_by_price(request,more,less):
    """
    List all code products,or create a new product
    """
    
    products = Product.objects.filter( price__gte=more,price__lte=less)
    #products = products.filter(price__gte=less)
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)
     




@api_view(['POST'])
def like_create_api(request,pk):
    product = get_object_or_404(Product.objects.all(), pk=pk)
    if (request.user in product.users_like.all()):
        product.users_like.remove(request.user)
    else:
        product.users_like.add(request.user)    
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# # class ProductHighlight(generics.GenericAPIView):
# #     queryset = Product.objects.all()
# #     renderer_classes = [renderers.StaticHTMLRenderer]
# #     def get(self,request,*args,**kwargs):
# #         product = self.get_object()
# #         return Response(snippet.highlishted)




# class ProductList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     """
#     List all product, or create a new product
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     def get(self,request,*args,**kwargs):
#         #product = Product.objects.all()
#         #serializer = ProductSerializer(product,many=True)
#         #return Response(serializer.data)
#         return self.list(request,*args,**kwargs)

#     def post(self,request,format=None):
#         # serializer = ProductSerializer(data = request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data,status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)        
#         return self.create(request,*args,**kwargs)

# class ProductDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     """
#     Retrieve, update or delete a  product instance 
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # def get_object(self,pk):
#     #     try:
#     #         return Product.objects.get(pk=pk)
#     #     except Product.DoesNotExist:
#     #         raise Http404


#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#         # product = self.get_object(pk)
#         # serializer = ProductSerializer(product)
#         # return Response(serializer.data)

#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#         # product = self.get_object(pk)
#         # serializer = ProductSerializer(product,data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data)
#         # return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
#         # product = self.get_object(pk)
#         # product.delete()
#         # return Response(status=status.HTTP_204_NO_CONTENT)            





# @api_view(['GET', 'POST'])
# def new_product_list(request):
#     """
#     List all code products,or create a new product
#     """
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)        
    
        
# @api_view(['GET', 'POST', 'DELETE'])
# def new_product_detail(request,pk):
    
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status.status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(product,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)        




def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug = category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category':category,
                   'categories':categories,
                   'products':products})



def base_view(request):
    categories = Category.objects.all()
    return render(request,
                  'shop/base.html',
                  {'categories':categories})

from .forms import LikeForm
def like(request,product_id):
    product = Product.objects.get(id=product_id)
    form = LikeForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['like']:
          product.users_like.add(request.user)
    return redirect('shop:product_list')



def product_detail(request,id,slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    like_product_form = LikeForm()
    
    user = Product.objects.filter(users_like__username = request.user.username)
    
    liked = True 
     
    product_tags_ids = product.tags.values_list('id',flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags_ids)\
                                       .exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags'))\
                                     .order_by('-same_tags','-updated')[:4]                                    
    return render(request,
                  'shop/product/detail.html',
                  {'product':product,
                   'similar_products':similar_products,
                   'liked':liked,
                   'cart_product_form': cart_product_form,
                   'like_product_form':like_product_form})



def search_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/search_results.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})




class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/product/search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(name__icontains=query)
        )

  
class ProductCreateView(CreateView):
    model = Product
    template_name = 'shop/product/product_new.html'
    fields = ('category','name','slug','image','description','price')
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)




from django.http import JsonResponse
from django.views.decorators.http import require_POST 
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def product_like(request):
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    if product_id and action:
        try:
            product = Product.objects.get(id=product_id)
            if action == 'like':
                product.users_like.remove(request.user)
            else:
                product.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})

from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from .forms import SearchForm

# def product_search(request):

#   query = None
#   results = []

#   query = request.GET.get('q') 
#   search_vector = SearchVector('name','description')
#   search_query = SearchQuery(query)
#   results = Product.objects.annotate(
#     )
#         similarity=TrigramSimilarity('name',query),
#         ).filter(similarity__gt=0.1).order_by('-similarity')
#   return render(request,
#                 'shop/product/search.html',
#                 {'query':query,
#                 'results':results})    

