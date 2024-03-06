from rest_framework import serializers
from contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'mail_from', 'content', 'full_name']

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mail_from = validated_data.get('mail_from', instance.mail_from)
        instance.content = validated_data.get('content', instance.content)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance
