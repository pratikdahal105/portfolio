from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from work.models import Work
from .serializers import WorkSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def work_list_create(request):
    if request.method == 'GET':
        works = Work.objects.filter(user=request.user)
        serializer = WorkSerializer(works, many=True)
        return Response({"status": True, "message": "Work list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Work created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Work creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def work_detail(request, id):
    try:
        work = Work.objects.get(id=id)
    except Work.DoesNotExist:
        return Response({"status": False, "message": "Work not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.user != work.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = WorkSerializer(work)
        return Response({"status": True, "message": "Work retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = WorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Work updated.", "data": serializer.data})
        return Response({"status": False, "message": "Work update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        work.delete()
        return Response({"status": True, "message": "Work deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
