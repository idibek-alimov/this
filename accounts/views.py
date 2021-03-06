from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from .models import Profile
from .forms import LoginForm,UserRegistrationForm
from shop.models import Product



"""
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('shop:product_list')
    template_name = 'registration/signup.html'
"""

"""
# Create your views here.
class ProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/profile.html'

"""
# new versions
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm
"""

"""
def user_login(request):
    if request.method == 'POSt':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated'\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})
"""



from  django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    products = Product.objects.filter(owner__username=request.user.username)
    liked = Product.objects.filter(users_like__username=request.user.username)
    return render(request,
                  'account/dashboard.html',
                  {'section':'dashboard',
                   'liked': liked,
                   'products':products})



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
                 # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

from .forms import UserEditForm,ProfileEditForm


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form':user_form,
                   'profile_form':profile_form})
