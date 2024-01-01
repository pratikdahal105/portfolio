from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from education.models import Education
from .serializers import EducationSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def education_list_create(request):
    if request.method == 'GET':
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response({"status": True, "message": "Education list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Education created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Education creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def education_detail(request, id):
    try:
        education = Education.objects.get(id=id)
    except Education.DoesNotExist:
        return Response({"status": False, "message": "Education not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.user != education.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = EducationSerializer(education)
        return Response({"status": True, "message": "Education retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Education updated.", "data": serializer.data})
        return Response({"status": False, "message": "Education update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        education.delete()
        return Response({"status": True, "message": "Education deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
