# views.pyssss
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Faculty
from Departments.models import Subject as DepartmentSubject
import json
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static
from django.core import serializers
from .serializers import FacultySerializer
from django.views.decorators.csrf import csrf_protect
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect





from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from .models import Faculty
from .serializers import FacultySerializer  # Assuming you have a serializer for the Faculty model
@csrf_exempt
def faculty_login(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            id_number = request.POST.get('id_number')
            password = request.POST.get('password')

            print(f"Login request for ID: {id_number}")

            # Check if the user with the given id_number exists
            faculty = Faculty.objects.filter(id_number=id_number).first()
            if faculty is None:
                print(f"Invalid ID number: {id_number}")
                return JsonResponse({'error': 'Invalid ID number'}, status=401)

            # Check the hashed password
            if not check_password(password, faculty.password):
                print(f"Invalid password for ID: {id_number}")
                return JsonResponse({'error': 'Invalid password'}, status=401)

            # At this point, authentication is successful
            # Log in the authenticated faculty
            login(request, faculty)
            print(f"Login successful for ID: {id_number}")

            # Serialize faculty information and include it in the response
            faculty_data = {
        'id_number': faculty.id_number,
        'first_name': faculty.first_name,
        'last_name': faculty.last_name,
        'status': faculty.status,
        'password': faculty.password,
        'selected_image': request.build_absolute_uri(faculty.selected_image.url) if faculty.selected_image else None,
        'subjects': [subject.Subname for subject in faculty.subjects.all()],
    }
            redirect_url = "http://52.63.82.248:3000/homepage"

            response_data = {
                'message_1': 'Login successful',
                'faculty': faculty_data,
                'redirect_url': redirect_url,
            }

            return JsonResponse(response_data)  # Add this line to return the response

        except IntegrityError as e:
            print(f"Error during login: {e}")
            return JsonResponse({'error': 'Duplicate entry. This ID number already exists.'}, status=400)

    else:
        print("Error: Only POST and GET requests are allowed")
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)
    


@csrf_exempt

def save_faculty(request):
    if request.method == 'POST':
        try:
            # Extract form data
            id_number = request.POST.get('id_number')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            status = request.POST.get('status')
            selected_subject_ids = request.POST.getlist('selected_subjects')
            
            # Check if the request contains a file
            if 'selected_image' in request.FILES:
                selected_image = request.FILES['selected_image']
            else:
                selected_image = None

            # Check if required fields are not empty
            if not id_number:
                return JsonResponse({'error': 'ID number cannot be empty'}, status=400)

            if not first_name or not last_name:
                return JsonResponse({'error': 'First name and Last name cannot be empty'}, status=400)

            if not status:
                return JsonResponse({'error': 'Status cannot be empty'}, status=400)

            # Validate subject IDs
            invalid_subject_ids = []
            for subject_id in selected_subject_ids:
                try:
                    # Check if the subject exists in the departments app
                    DepartmentSubject.objects.get(id=subject_id)
                except DepartmentSubject.DoesNotExist:
                    invalid_subject_ids.append(subject_id)

            if invalid_subject_ids:
                return JsonResponse({'error': f'Invalid subject IDs: {invalid_subject_ids}'}, status=400)

            # Create and save the faculty
            password_hash = make_password(password)
            faculty = Faculty.objects.create(
                id_number=id_number,
                first_name=first_name,
                last_name=last_name,
                password=password_hash,
                status=status,
                selected_image=selected_image  # Save the image file
            )

            # Associate selected subjects with the faculty member
            for subject_id in selected_subject_ids:
                try:
                    subject = DepartmentSubject.objects.get(id=subject_id)
                    faculty.subjects.add(subject)
                except DepartmentSubject.DoesNotExist:
                    # Handle the case where the subject does not exist
                    return JsonResponse({'error': f'Subject with ID {subject_id} does not exist'}, status=400)

            return JsonResponse({'message': 'Faculty data saved successfully'}, status=201)

        except IntegrityError:
            return JsonResponse({'error': 'Duplicate entry. This ID number already exists.'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)





    
def show_all_faculty(request):
    faculties = Faculty.objects.all()
    serializer = FacultySerializer(faculties, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)

    


@csrf_protect
def delete_all_faculty_records(request):
    try:
        # Retrieve all faculty records
        faculties = Faculty.objects.all()

        # Loop through each faculty record
        for faculty in faculties:
            # Delete associated image file if it exists
            if faculty.selected_image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(faculty.selected_image))
                if os.path.exists(image_path):
                    os.remove(image_path)

            # Remove all associated subjects
            faculty.subjects.clear()

            # Delete the faculty record
            faculty.delete()

        return JsonResponse({'message': 'All faculty records deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def faculty_info(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)

    # Customize this dictionary based on your Faculty model fields
    faculty_info = {
        'id_number': faculty.id_number,
        'first_name': faculty.first_name,
        'last_name': faculty.last_name,
        'status': faculty.status,
        'password': faculty.password,
        'selected_image': request.build_absolute_uri(faculty.selected_image.url) if faculty.selected_image else None,
        'subjects': [subject.Subname for subject in faculty.subjects.all()],
    }


    return JsonResponse(faculty_info)