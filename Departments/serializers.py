from rest_framework import serializers
from .models import Departments, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'Subname','SubDescriptions')

class DepartmentSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Departments
        fields = ('id', 'CodeName', 'Descriptions','subjects')