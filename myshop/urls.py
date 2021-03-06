"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view 

API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for creating and editing products.'
schema_view = get_swagger_view(title =API_TITLE)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',include('cart.urls',namespace='cart')),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('api/',include('api.urls',namespace='api')),
    path('api_auth/',include('rest_framework.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', # new
                      include('rest_auth.registration.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    #path('schema/',schema_view), 
   
    path('docs/',include_docs_urls(title =API_TITLE,
                                   description=API_DESCRIPTION)),
    path('swagger-docs/',schema_view),
    path('',include('shop.urls',namespace='shop')),
   
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)
