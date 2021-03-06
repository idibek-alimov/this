from django.urls import path
from .views import page_view

urlpatterns = [
    path('',page_view,name='pages'),
]