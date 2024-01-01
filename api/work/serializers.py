from rest_framework import serializers
from work.models import Work

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'user', 'company_name', 'job_title', 'location', 'start_date', 'end_date', 'description']

    def create(self, validated_data):
        return Work.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.location = validated_data.get('location', instance.location)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
