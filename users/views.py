from django.shortcuts import render
from .models import Profile

def login_page(request):
    return render(request, 'users/login_register.html')

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
