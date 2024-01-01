from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from .serializers import ProjectSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def project_list_create(request):
    if request.method == 'GET':
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response({"status": True, "message": "Project list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Project created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Project creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def project_detail(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response({"status": False, "message": "Project not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.user != project.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response({"status": True, "message": "Project retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Project updated.", "data": serializer.data})
        return Response({"status": False, "message": "Project update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response({"status": True, "message": "Project deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
