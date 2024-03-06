from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from contact.models import Contact
from .serializers import ContactSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token
from django.utils import timezone

@api_view(['GET', 'POST'])
def contact_list_create(request):
    try:
        username = request.POST.get('username')
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)
    if user:
        if request.method == 'GET':
            contacts = Contact.objects.filter(user=user)
            serializer = ContactSerializer(contacts, many=True)
            return Response({"status": True, "message": "Contact list retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        # Retrieve user session
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        # Retrieve last request timestamp from session
        last_request_time = request.session.get('last_request_time')

        # Check if last request time exists and compare with current time
        if last_request_time and (timezone.now() - last_request_time).total_seconds() < 120:  # 120 seconds = 2 minutes
            return Response({"status": False, "message": "Rate limit exceeded. Try again later."}, status=429)

        # Update last request time in session
        request.session['last_request_time'] = timezone.now()

        # Your existing code to handle contact creation
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"status": True, "message": "Contact created.", "data": serializer.data}, status=201)
        return Response({"status": False, "message": "Contact creation failed.", "data": serializer.errors}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def contact_detail(request, id):
    try:
        user = request.user
        contact = Contact.objects.get(id=id, user=user)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)
    except Contact.DoesNotExist:
        return Response({"status": False, "message": "Contact not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response({"status": True, "message": "Contact retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Contact updated.", "data": serializer.data})
        return Response({"status": False, "message": "Contact update failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response({"status": True, "message": "Contact deleted.", "data": None}, status=status.HTTP_204_NO_CONTENT)
