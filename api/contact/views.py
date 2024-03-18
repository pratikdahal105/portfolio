from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from contact.models import Contact
from .serializers import ContactSerializer
from api.profile.decorators import require_authenticated_and_valid_token as valid_token
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail

@api_view(['GET', 'POST'])
def contact_list_create(request):
    try:
        username = request.data.get('username')
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found.", "data": None}, status=status.HTTP_404_NOT_FOUND)
    
    if user:
        if request.method == 'GET':
            contacts = Contact.objects.filter(user=user)
            serializer = ContactSerializer(contacts, many=True)
            return Response({"status": True, "message": "Contact list retrieved.", "data": serializer.data})

        elif request.method == 'POST':
            # Pass the user to the serializer
            serializer = ContactSerializer(data=request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                
                # Fetch email details from frontend payload
                subject = request.data.POST.get('subject')
                message = request.data.POST.get('message')
                from_email = request.data.POST.get('from_email')

                # Send email notification to the user
                send_contact_notification_email(user, subject, message, from_email)
                
                return Response({"status": True, "message": "Contact created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": "Contact creation failed.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({"status": False, "message": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def send_contact_notification_email(user, subject, message, from_email):
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

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
