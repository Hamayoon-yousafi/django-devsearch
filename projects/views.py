from django.shortcuts import render
 
def projects(request):
    return render(request, 'projects/projects.html')


def project(request, id):
    values = {
        'project': id
    }
    return render(request, 'projects/single-project.html', values)
