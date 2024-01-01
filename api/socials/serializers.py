from rest_framework import serializers
from socials.models import Socials

class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socials
        fields = ['id', 'user', 'account_name', 'logo', 'link']

    def create(self, validated_data):
        return Socials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.account_name = validated_data.get('account_name', instance.account_name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance
