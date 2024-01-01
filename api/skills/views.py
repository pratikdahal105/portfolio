from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from skills.models import Skill
from .serializers import SkillSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token

@api_view(['GET', 'POST'])
@valid_token
def skill_list_create(request):
    if request.method == 'GET':
        skills = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(skills, many=True)
        return Response({"status": True, "message": "Skill list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "message": "Skill created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Skill creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def skill_detail(request, id):
    try:
        skill = Skill.objects.get(id=id)
    except Skill.DoesNotExist:
        return Response({"status": False, "message": "Skill not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.user != skill.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return Response({"status": True, "message": "Skill retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Skill updated.", "data": serializer.data})
        return Response({"status": False, "message": "Skill update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        skill.delete()
        return Response({"status": True, "message": "Skill deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
