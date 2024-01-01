from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from awards.models import Award
from api.awards.serializers import AwardSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def award_list_create(request):
    if request.method == 'GET':
        user = request.user
        awards = Award.objects.filter(user)
        return Response({"status": True, "message": "Award list retrieved.", "data": awards})

    elif request.method == 'POST':
        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Award created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Award creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def award_detail(request, id):
    try:
        award = Award.objects.get(id=id)
    except Award.DoesNotExist:
        return Response({"status": False, "message": "Award not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.user != award.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = AwardSerializer(award)
        return Response({"status": True, "message": "Award retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = AwardSerializer(award, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Award updated.", "data": serializer.data})
        return Response({"status": False, "message": "Award update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        award.delete()
        return Response({"status": True, "message": "Award deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)