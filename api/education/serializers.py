from rest_framework import serializers
from education.models import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'user', 'school_name', 'school_location', 'degree', 'major', 'gpa', 'start_date', 'end_date', 'image', 'description']

    def create(self, validated_data):
        return Education.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.school_name = validated_data.get('school_name', instance.school_name)
        instance.school_location = validated_data.get('school_location', instance.school_location)
        instance.degree = validated_data.get('degree', instance.degree)
        instance.major = validated_data.get('major', instance.major)
        instance.gpa = validated_data.get('gpa', instance.gpa)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
