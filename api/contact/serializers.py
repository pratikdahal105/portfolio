from rest_framework import serializers
from contact.models import Contact
from django.contrib.auth.models import User

class ContactSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=255, write_only=True)  # Add subject field as write-only

    class Meta:
        model = Contact
        fields = ['id', 'mail_from', 'content', 'subject']  # Replace 'full_name' with 'subject'

    def create(self, validated_data):
        # Retrieve the user from the context
        user = self.context.get('user')

        # Manipulate the validated data to store subject in place of full_name
        validated_data['full_name'] = validated_data.pop('subject')

        # Set the user field of the contact instance
        validated_data['user'] = user

        # Create and return the contact instance
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mail_from = validated_data.get('mail_from', instance.mail_from)
        instance.content = validated_data.get('content', instance.content)
        instance.full_name = validated_data.get('subject', instance.full_name)  # Update subject field
        instance.save()
        return instance
