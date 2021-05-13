from django.urls import path
from . import views
from api.views import SearchListView ,Profile,LikedProducts,product_create,ProfileView,\
     preference_create
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'shop'

urlpatterns = [
     path('prefcret',preference_create,name='pref_cret'),
     path('filtering',views.FilterListView.as_view(),name='filter_list_view'),
     path('profileview',ProfileView.as_view(),name='profile_view'),
     #path('createproductagin',ProductCreateAPIView.as_view(),name='create_a_product_again'),
     path('createproduct/',product_create,name='create_a_product'),
     #path('createproduct/',CreateProduct.as_view(),name='create_a_product'),
     path('searchbytext/<str:query>/',views.search_by_url_text,name='search_by_url_text'),
     path('pricefilter/<int:more>/<int:less>',views.product_filter_by_price,name='price_filter'),
     path('likeaproduct/<int:pk>',views.like_create_api,name='like_thing'),
     path('likedproducts',LikedProducts.as_view(),name='liked_products'),
     path('profileapi/',Profile.as_view(),name='profile_view'),
     #path('searchapilist/',ProductSearchList.as_view(),name='product_search_list'),
   # path('api_root/'views.api_root,name='api_root'),
    #path('prodcuts/<int:pk>/highlight/',views.ProductHighlight.as_view(),name='product_highlight'), 
#     path('classproduct/',views.ProductList.as_view(),name='class_product'),
#     path('classproduct/<int:pk>/',views.ProductDetail.as_view(),name='class_productpk'), 
#     path('newdetail/<int:pk>',views.new_product_detail,name='new_product_detail'), 
#     path('listapi/',views.new_product_list,name='new_product_list'), 
   # path('searchapi/',SearchListView.as_view(),name='searchapi'), 
    path('likee/<str:product_id>/',views.like,name='likee'),
    path('like/',views.product_like,name='like'),
#     path('search1/',views.product_search,name='search_results1'),
    path('base/',views.base_view,name='base_view'),
    path('search/',views.SearchResultsListView.as_view(),
         name='search_results'),
    path('searches/',views.search_list,
         name='search_list'),
    path('new/',views.ProductCreateView.as_view(),name='product_new'),
    path('',views.product_list,name='product_list'),
    path('<slug:category_slug>/',views.product_list,
          name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',views.product_detail,
         name='product_detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
