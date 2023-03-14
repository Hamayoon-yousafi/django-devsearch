from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm

def projects(request): 
    return render(request, 'projects/projects.html', {'projects': Project.objects.all()})

def project(request, id): 
    return render(request, 'projects/single-project.html', {'project': Project.objects.get(id=id)})

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) # contains all the data which was sent by the post
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    values = {
        'form': form
    }
    return render(request, 'projects/project_form.html', values)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project) # contains all the data which was sent by the post
        if form.is_valid():
            form.save()
            return redirect('account')

    values = {
        'form': form
    }
    return render(request, 'projects/project_form.html', values) 

@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    values = {
        'object': project
    }
    return render(request, 'delete_template.html', values)