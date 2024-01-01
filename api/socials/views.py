from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from socials.models import Socials
from .serializers import SocialsSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def socials_list_create(request):
    if request.method == 'GET':
        socials = Socials.objects.filter(user=request.user)
        serializer = SocialsSerializer(socials, many=True)
        return Response({"status": True, "message": "Socials list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = SocialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Social created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Social creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def socials_detail(request, id):
    try:
        social = Socials.objects.get(id=id)
    except Socials.DoesNotExist:
        return Response({"status": False, "message": "Social not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    # Check if the social account belongs to the authenticated user
    if request.user != social.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = SocialsSerializer(social)
        return Response({"status": True, "message": "Social retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = SocialsSerializer(social, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Social updated.", "data": serializer.data})
        return Response({"status": False, "message": "Social update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        social.delete()
        return Response({"status": True, "message": "Social deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
