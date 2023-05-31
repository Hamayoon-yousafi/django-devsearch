from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review

@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        # token routes. generate token and refresh token 
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # only login users can access this route
def project_vote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # get_or_create will check the database if such project exists, if not it creates it. The second variable (created) will be boolean and True if new instance is created.
    review, created = Review.objects.create( 
        owner=user,
        project=project,
    )

    review.value = data.get('value')
    review.body = data.get('body')
    review.save()
    project.get_vote_count

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)