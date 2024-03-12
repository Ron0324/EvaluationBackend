import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Course, Student
from .serializers import CourseSerializer,StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login




@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Hash the password before saving
        hashed_password = make_password(data['password'])

        student = Student.objects.create(
            id_number=data['id_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            suffix=data['suffix'],
            password=hashed_password,
            course=data['course']
        )

        return JsonResponse({'message': 'Student created successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    


@csrf_exempt
@require_POST
def save_course(request):
    try:
        data = json.loads(request.body)
        course_name = data.get('course_name')
        description = data.get('description')
        department = data.get('department')

        # Check if course_name is present and not empty
        if course_name is None or course_name.strip() == '':
            return JsonResponse({'message': 'Course name is required'}, status=400)

        # Save to the database using the Course model
        course = Course(course_name=course_name, description=description, department=department)
        course.save()

        # Serialize the saved instance for the response
        serializer = CourseSerializer(course)
        serialized_data = serializer.data

        return JsonResponse({'message': 'Course saved successfully', 'data': serialized_data})
    except IntegrityError:
        return JsonResponse({'message': 'Duplicate entry. Course not saved.'}, status=400)
    

@csrf_exempt
def show_courses(request):
    courses = Course.objects.all().values()
    return JsonResponse(list(courses), safe=False)
@csrf_exempt
def show_Students(request):
    student = Student.objects.all().values()
    return JsonResponse(list(student), safe=False)
   

@csrf_exempt
def student_login(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            # Ensure there is data in the request body
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)

            # Attempt to load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            id_number = data.get('id_number', '')
            password = data.get('password', '')

            # Check if the user with the given id_number exists
            student = Student.objects.filter(id_number=id_number).first()
            if student is None:
                return JsonResponse({'error': 'Invalid ID number'}, status=401)

            # Check the hashed password
            if not check_password(password, student.password):
                return JsonResponse({'error': 'Invalid password'}, status=401)

            # At this point, authentication is successful
            # Log in the authenticated student
            login(request, student)

    # Include the redirect URL in the response
            redirect_url = "http://52.63.82.248:3000/homepage"
            print('Login successful. Redirecting to:', redirect_url)

            return JsonResponse({'message': 'Login successful', 'redirect_url': redirect_url})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except IntegrityError as e:
            return JsonResponse({'error': 'Duplicate entry. This ID number already exists.'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)






#marked
    



   