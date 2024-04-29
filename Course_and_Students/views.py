import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Course, Student,Admin
from .serializers import CourseSerializer,StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login ,authenticate





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
def create_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Hash the password before saving
        hashed_password = make_password(data['password'])

        admin = Admin.objects.create(
            id_number=data['id_number'],
            full_name=data ['full_name'],
            password=hashed_password,
            
        )

        return JsonResponse({'message': 'Student created successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    




@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        try:
            id_number = request.POST.get('id_number')
            password = request.POST.get('password')

            print(f"Login request for ID: {id_number}")

            # Check if the user with the given id_number exists
            admin = Admin.objects.filter(id_number=id_number).first()
            if admin is None:
                print(f"Invalid ID number: {id_number}")
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            # Check the hashed password
            if not check_password(password, admin.password):
                print(f"Invalid password for ID: {id_number}")
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            # At this point, authentication is successful
            # Log in the authenticated admin
            login(request, admin)
            print(f"Login successful for ID: {id_number}")

            # Serialize admin information
            admin_data = {
                'id_number': admin.id_number,
                'first_name': admin.first_name,
                # Add more fields as needed
            }

            # Redirect URL after successful login
            redirect_url = "http://91.108.111.180:3000/Admin-Dashboard"

            response_data = {
                'message': 'Login successful',
                'admin': admin_data,
                'redirect_url': redirect_url,
            }

            return JsonResponse(response_data)

        except IntegrityError as e:
            print(f"Error during login: {e}")
            return JsonResponse({'error': 'Database error'}, status=500)

    else:
        print("Error: Only POST requests are allowed")
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


    


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
def show_admins(request):
    admin = Admin.objects.all().values()
    return JsonResponse(list(admin), safe=False)

@csrf_exempt
def admin_update(request):
    if request.method == 'POST':
        try:
            # Deserialize the JSON data sent in the request body
            data = json.loads(request.body)
            
            # Extract the admin id from the data
            admin_id = data.get('id')  # Assuming 'id' is the primary key field
            
            # Retrieve the admin object from the database
            admin = Admin.objects.get(pk=admin_id)
            
            # Update the admin object with the new information
            admin.id_number = data.get('id_number', admin.id_number)
            admin.full_name = data.get('full_name', admin.full_name)
            
            # Hash the new password before saving
            new_password = data.get('password')
            if new_password:
                admin.password = make_password(new_password)
            
            # Save the updated admin object
            admin.save()
            
            return JsonResponse({'message': 'Admin information updated successfully'})
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

@csrf_exempt
def admin_delete(request, admin_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the admin object from the database
            admin = Admin.objects.get(pk=admin_id)
            
            # Delete the admin object
            admin.delete()
            
            return JsonResponse({'message': 'Admin deleted successfully'})
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)
   

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
            redirect_url = "http://91.108.111.180:3000/homepage"
            print('Login successful. Redirecting to:', redirect_url)

            return JsonResponse({'message': 'Login successful', 'redirect_url': redirect_url})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except IntegrityError as e:
            return JsonResponse({'error': 'Duplicate entry. This ID number already exists.'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)






#marked
    



   