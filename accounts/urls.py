from django.urls import path
from .views import user_login ,dashboard,register,edit
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    #path('profile/',ProfileView.as_view(),name='profile'),
    #path('signup/',SignUpView.as_view(),name='signup'),
    path('register/',register,name='register'),
    #path('new_login/',user_login,name='new_login'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('edit/',edit,name='edit'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('',dashboard,name='dashboard'),
]