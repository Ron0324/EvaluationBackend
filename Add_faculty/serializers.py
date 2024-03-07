from rest_framework import serializers
from .models import Faculty
from Departments.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['Subname','SubDescriptions','department', ]

class FacultySerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()  # Use SerializerMethodField for custom handling

    class Meta:
        model = Faculty
        fields = ['id', 'id_number', 'first_name', 'last_name', 'status', 'selected_image', 'subjects']

    def get_subjects(self, obj):
        # Retrieve subjects associated with the faculty
        subjects_queryset = obj.subjects.all()
        # Serialize the subjects
        subjects_serializer = SubjectSerializer(subjects_queryset, many=True)
        return subjects_serializer.data
