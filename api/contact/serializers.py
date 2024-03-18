from rest_framework import serializers
from contact.models import Contact
from django.contrib.auth.models import User

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'mail_from', 'content', 'full_name']

    def create(self, validated_data):
        # Retrieve the user from the context
        user = self.context.get('user')

        # Set the user field of the contact instance
        validated_data['user'] = user

        # Create and return the contact instance
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mail_from = validated_data.get('mail_from', instance.mail_from)
        instance.content = validated_data.get('content', instance.content)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance
