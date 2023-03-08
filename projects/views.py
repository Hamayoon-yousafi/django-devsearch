from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

def projects(request): 
    return render(request, 'projects/projects.html', {'projects': Project.objects.all()})

def project(request, id): 
    return render(request, 'projects/single-project.html', {'project': Project.objects.get(id=id)})

def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) # contains all the data which was sent by the post
        if form.is_valid():
            form.save()
            return redirect('projects')

    values = {
        'form': form
    }
    return render(request, 'projects/project_form.html', values)

def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project) # contains all the data which was sent by the post
        if form.is_valid():
            form.save()
            return redirect('projects')

    values = {
        'form': form
    }
    return render(request, 'projects/project_form.html', values) 

def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    values = {
        'object': project
    }
    return render(request, 'projects/delete_template.html', values)