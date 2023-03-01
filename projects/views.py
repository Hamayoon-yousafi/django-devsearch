from django.shortcuts import render
from django.http import HttpResponse


def projects(request):
    return HttpResponse('These are different products.')


def project(request, id):
    return HttpResponse(f'returned project with id {id}')
