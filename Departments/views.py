from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Departments,Subject
from .serializers import DepartmentSerializer

class DepartmentListAPIView(generics.ListAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer



@csrf_exempt
@require_POST  # Use this decorator to ensure the view only responds to POST requests
def save_multiple_subjects(request, department_id):
    if request.method == 'POST':
        try:
            subjects_data = json.loads(request.body.decode('utf-8'))['subjects_data']
            department = Departments.objects.get(pk=department_id)
            
            for subject_data in subjects_data:
                subject = Subject.objects.create(Subname=subject_data['Subname'], SubDescriptions=subject_data['SubDescriptions'], department=department)
            
            return JsonResponse({'message': 'Subjects saved successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
@require_POST
def save_department(request):
   
        try:
            data = json.loads(request.body)
            code_name = data.get('CodeName')
            description = data.get('Descriptions')

            # Check if CodeName is present and not empty
            if code_name is None or code_name.strip() == '':
                return JsonResponse({'message': 'CodeName is required'}, status=400)

            # Save to the database using the AddDepartment model
            department = Departments(CodeName=code_name, Descriptions=description)
            department.save()

            return JsonResponse({'message': 'Department saved successfully'})
        except IntegrityError:
            return JsonResponse({'message': 'Duplicate entry. Department not saved.'}, status=400)


@csrf_exempt
def show_departments(request):
    departments = Departments.objects.all().values()  # Convert QuerySet to values
    return JsonResponse(list(departments), safe=False)

@csrf_exempt
def show_subjects(request):
    subjects= Subject.objects.all().values()  # Convert QuerySet to values
    return JsonResponse(list(subjects), safe=False)


def show_subjects_by_department(request, department_id):
    # Retrieve the department instance or return a 404 error if it doesn't exist
    department = get_object_or_404(Departments, id=department_id)
    
    # Filter subjects based on the department
    subjects = Subject.objects.filter(department=department).values()
    
    # Return JSON response with the list of subjects
    return JsonResponse(list(subjects), safe=False)