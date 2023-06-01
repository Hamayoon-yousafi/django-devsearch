from django.shortcuts import render, redirect
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from .filters import ProjectFilter
from .utils import pagination
from django.contrib import messages


def projects(request):  
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    projects = project_filter.qs # the qs stands for Query Set and returns all the records searched for

    last_page, pages, projects = pagination(projects, request.GET.get('page'))

    values = {
        'projects': projects, 
        'project_filter': project_filter,  
        'last_page': last_page,
        'pages': pages,
        'search': request.GET.get('search') or ''
    }
    return render(request, 'projects/projects.html', values)

def project(request, id):
    form = ReviewForm()
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        # update project vote count
        project.get_vote_count # this is the property method on Project model

        messages.success(request, 'Your review was submitted!')
        return redirect('project', id=project.id)
    return render(request, 'projects/single-project.html', {'project': project, 'form': form})

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES) # contains all the data which was sent by the post
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for newtag in newtags:
                tag, created = Tag.objects.get_or_create(name=newtag)
                project.tags.add(tag)
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
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project) # contains all the data which was sent by the post
        if form.is_valid():
            project = form.save()
            for newtag in newtags:
                tag, created = Tag.objects.get_or_create(name=newtag)
                project.tags.add(tag)
            return redirect('account')

    values = {
        'form': form,
        'project': project
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