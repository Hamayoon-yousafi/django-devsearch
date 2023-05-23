from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, pagination

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password) # will check if user with this username and password exists
        if user:
            login(request, user) # this will make a session for the user and store session in the browser's cookies
            messages.success(request, 'Logged in successfully!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occured during registration!')

    values = {
        'page': 'register',
        'form': form
    }
    return render(request, 'users/login_register.html', values)

def profiles(request):
    profiles, search_query = search_profiles(request) 

    last_page, pages, profiles = pagination(profiles, request.GET.get('page'))

    values = {
        'profiles': profiles,
        'search_query': search_query,
        'last_page': last_page,
        'pages': pages,
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

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    values = {
        'profile': profile,
        'skills': profile.skill_set.all(),
        'projects': profile.project_set.all()
    }
    return render(request, 'users/account.html', values)

@login_required(login_url='login')
def edit_account(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated profile!')
            return redirect('account')

    values = {
        'form': form
    }
    return render(request, 'users/profile_form.html', values)

@login_required(login_url='login')
def create_skill(request):
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('account')
    values = { 
        'form': form
    }
    return render(request, 'users/skill_form.html', values)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill edited successfully!')
            return redirect('account')
    values = { 
        'form': form
    }
    return render(request, 'users/skill_form.html', values)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted Successfully!')
        return redirect('account')

    values = {
        'object': skill
    }
    return render(request, 'delete_template.html', values)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    values = {
        'message_requests': message_requests,
        'unread_count': unread_count
    }
    return render(request, 'users/inbox.html', values)

@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    values = {
        'message': message
    }
    return render(request, 'users/message.html', values)

def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Message sent successfully sent!')
            return redirect('user-profile', pk)

    values = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', values)