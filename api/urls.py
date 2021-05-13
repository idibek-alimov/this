from django.urls import path,include
from rest_framework.routers import SimpleRouter

from .views import  SearchListView,UserViewSet,ProductViewSet,CategoryViewSet,ProductByCategoryListView,SimilarTagsProduct,\
CategoryProductFilter,CartView,PreferencesViewSet,preference_create


app_name = 'api'

router = SimpleRouter()
#router.register('tags/<int:pk>/',SimilarTagsProduct)
router.register('category',CategoryViewSet)
router.register('users', UserViewSet)
router.register('cartview/',CartView)
router.register('preferences',PreferencesViewSet)
#router.register('search',SearchListView)
router.register('bycategory',ProductByCategoryListView)
router.register('', ProductViewSet)
urlpatterns =[
    path('',include(router.urls)),
    path('<int:category>/<str:search>/',CategoryProductFilter.as_view(),name='category_product_filter'),
    path('tags/<int:pk>/',SimilarTagsProduct.as_view(),name='tags'),
    path('createpreference/',preference_create,name='create_preference'),
  ]

#[
  #  path('users/',UserList.as_view()),
  #  path('users/<int:pk>/',UserDetail.as_view()),
  #  path('rest_auth/',include('rest_auth.urls')),
  #  path('<int:pk>/',DetailProduct.as_view()),
   # path('category/',CategoryListView.as_view()),
  #  path('api_auth/',include('rest_framework.urls')),
    
 #   path('',ListAPIView.as_view()),
    
#]
