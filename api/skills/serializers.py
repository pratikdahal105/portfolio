from rest_framework import serializers
from skills.models import Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'user', 'skill_name', 'description']

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.skill_name = validated_data.get('skill_name', instance.skill_name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
