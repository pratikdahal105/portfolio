from rest_framework import serializers
from awards.models import Award

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['user', 'award_name', 'description', 'award_date', 'awarded_by']

    def create(self, validated_data):
        return Award.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.award_name = validated_data.get('award_name', instance.award_name)
        instance.description = validated_data.get('description', instance.description)
        instance.award_date = validated_data.get('award_date', instance.award_date)
        instance.awarded_by = validated_data.get('awarded_by', instance.awarded_by)
        instance.save()
        return instance
