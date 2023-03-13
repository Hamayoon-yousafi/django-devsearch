from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password) # will check if user with this username and password exists
        if user:
            login(request, user) # this will make a session for the user and store session in the browser's cookies
            messages.success(request, 'Logged in successfully!')
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Passwords do not match!')

    return render(request, 'users/login_register.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'You were logged out successfully!')
    return redirect('login')

def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save() # this would save the form data but we want to make the username lower case so doing it as below
            user = form.save(commit=False) # this will return User instance but will not save it in DB
            user.username = user.username.lower() # make the username lower case
            user.save() # now this will actually save the user in the DB
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error occured during registration!')

    values = {
        'page': 'register',
        'form': form
    }
    return render(request, 'users/login_register.html', values)

def profiles(request):
    values = {
        'profiles': Profile.objects.all()
    }
    return render(request, 'users/profiles.html', values)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    values = {
        'profile': profile,
        'top_skills': profile.skill_set.exclude(description__exact=''),
        'other_skills': profile.skill_set.filter(description='')
    }
    return render(request, 'users/user-profile.html', values)