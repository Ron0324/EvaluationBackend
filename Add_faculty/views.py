# views.pyssss
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Faculty, Evaluation, FacultySubject
from Departments.models import Subject as DepartmentSubject
from Departments.models import Subject
from Departments.models import Semester
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
from django.views.decorators.http import require_POST
from textblob import TextBlob
from django.shortcuts import render
import re 

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Faculty, FacultySubject,  newEvaluation
from Course_and_Students.models import Student





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
            redirect_url = "http://91.108.111.180:3000/Instructors-Homepage"

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
def save_faculty_subjects(request, faculty_id):
    if request.method == 'POST':
        # Extract form data from the request
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        subject_ids = request.POST.getlist('subjects')

        # Get the faculty member based on the provided ID
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)

        # Save subjects for the faculty member
        for subject_id in subject_ids:
            FacultySubject.objects.create(
                faculty=faculty,
                subject_id=subject_id,
                year=year,
                semester=semester
            )

        return JsonResponse({'message': 'Subjects saved successfully'}, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def faculty_subjects(request, faculty_id, year, semester):
    if request.method == 'GET':
        try:
            # Get the faculty object or raise a 404 error if not found
            faculty = get_object_or_404(Faculty, id=faculty_id)
            
            # Convert semester input to integer
            semester = int(semester)
            
            # Ensure semester input is within valid range (1 or 2)
            if semester not in [1, 2]:
                return JsonResponse({'error': 'Invalid semester value'}, status=400)
            
            # Retrieve the subjects associated with the faculty for the given year and semester
            faculty_subjects = FacultySubject.objects.filter(faculty=faculty, year=year, semester=semester)
            
            # Extract the subjects from the faculty_subjects queryset
            subjects = [faculty_subject.subject.Subname for faculty_subject in faculty_subjects]
            
            # Return a JSON response with the list of subjects
            return JsonResponse({'subjects': subjects})
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Faculty, FacultySubject

def fetch_subjects(request, faculty_id, year, semester):
    if request.method == 'GET':
        try:
            # Get the faculty object or return a 404 error if not found
            faculty = get_object_or_404(Faculty, id=faculty_id)
            
            # Convert semester input to integer
            semester = int(semester)
            
            # Ensure semester input is within valid range (1 or 2)
            if semester not in [1, 2]:
                return JsonResponse({'error': 'Invalid semester value'}, status=400)

            # Retrieve the subjects associated with the faculty for the given year and semester
            faculty_subjects = FacultySubject.objects.filter(
                faculty=faculty,
                year=year,
                semester=semester
            )

            # Extract the subjects from the faculty_subjects queryset
            subjects = [
                {'id': faculty_subject.subject.id, 'name': faculty_subject.subject.Subname}
                for faculty_subject in faculty_subjects
            ]

            # Return a JSON response with the list of subjects
            return JsonResponse({'subjects': subjects})
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def fetch_evaluations(request, faculty_id, subject_id, year, semester):
    try:
        # Query evaluations for the specified faculty, subject, year, and semester
        evaluations = newEvaluation.objects.filter(
            faculty_id=faculty_id,
            subject_id=subject_id,
            year=year,
            semester=semester
        ).values(
            'criteria_A', 'criteria_B', 'criteria_C', 'criteria_D', 'total_rate', 'feedback'
        )

        # Calculate average total_rate
        average_rating = newEvaluation.objects.filter(
            faculty_id=faculty_id,
            subject_id=subject_id,
            year=year,
            semester=semester
        ).aggregate(avg_rating=Avg('total_rate'))['avg_rating']

        # Convert QuerySet to list of dictionaries
        evaluations_list = list(evaluations)

        return JsonResponse({'evaluations': evaluations_list, 'average_rating': average_rating})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
@csrf_exempt
def get_years(request, faculty_id):
    try:
        # Get the distinct year values associated with the selected faculty member
        years = FacultySubject.objects.filter(faculty_id=faculty_id).values_list('year', flat=True).distinct()

        # Convert the queryset to a list of integers
        years = list(years)

        # Return the list of distinct years as JSON response
        return JsonResponse({'years': years})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def add_subjects_to_faculty(request):
    data = json.loads(request.body)
    faculty_id = data.get('id')  # Using 'id' directly
    semester = data.get('semester')
    year = data.get('year')
    subjects = data.get('subjects')

    # Retrieve the faculty instance
    faculty = Faculty.objects.get(id=faculty_id)

    # Add subjects to the faculty for the specified semester and year
    for subject_id in subjects:
        subject = DepartmentSubject.objects.get(id=subject_id)
        FacultySubject.objects.create(faculty=faculty, subject=subject, semester=semester, year=year)

    return JsonResponse({'success': True})


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

from decimal import Decimal
import logging


import logging

logger = logging.getLogger(__name__)
@csrf_exempt
@require_POST
def save_evaluation(request, faculty_id):
    if request.method == 'POST':
        try:
            evaluations_data = json.loads(request.body.decode('utf-8'))['evaluations_data']
            faculty = Faculty.objects.get(pk=faculty_id)

            for evaluation_data in evaluations_data:
                student_id = evaluation_data['student_id']
                semester_choice = evaluation_data['semester_choice']
                year = evaluation_data['year']
                subject_id = evaluation_data['subject_id']
                year_level=  evaluation_data['year_level']
                student_id_number = evaluation_data['student_id_number']
                criteria_A = Decimal(evaluation_data['criteria_A'])
                criteria_B = Decimal(evaluation_data['criteria_B'])
                criteria_C = Decimal(evaluation_data['criteria_C'])
                criteria_D = Decimal(evaluation_data['criteria_D'])
                total_rate = evaluation_data['total_rate']
                feedback = evaluation_data['feedback']
                course = evaluation_data['course']

                student = Student.objects.get(id=student_id)

                # Check if the student has already evaluated this subject for the specified semester and year
                if newEvaluation.objects.filter(
                    student=student,
                    subject_id=subject_id,
                    semester=semester_choice,
                    year=year
                ).exists():
                    return JsonResponse({
                        'error': f'Student {student_id_number} has already evaluated this subject for semester {semester_choice} and year {year}.'
                    }, status=400)  # Send custom response for duplicate evaluation

                # Check the number of existing evaluations for the subject, semester, and year
                existing_evaluations_count = newEvaluation.objects.filter(
                    subject_id=subject_id,
                    semester=semester_choice,
                    year=year
                ).count()

                if existing_evaluations_count >= 30:
                    return JsonResponse({
                        'error': f'The maximum limit of 30 evaluators has been reached for this subject, semester, and year.'
                    }, status=400)

                evaluation = newEvaluation.objects.create(
                    faculty=faculty,
                    student=student,
                    subject_id=subject_id,
                    semester=semester_choice,
                    year=year,
                    year_level=year_level,
                    student_id_number=student_id_number,
                    criteria_A=criteria_A,
                    criteria_B=criteria_B,
                    criteria_C=criteria_C,
                    criteria_D=criteria_D,
                    total_rate=total_rate,
                    course=course,
                    feedback=feedback
                )

            return JsonResponse({'message': 'Evaluations saved successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Default error response
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


from django.db.models import Avg
def evaluation_score_per_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)

    # Fetching specific fields from Evaluation objects
    scores = Evaluation.objects.filter(faculty=faculty).values(
        'criteria_A', 'criteria_B', 'criteria_C', 'criteria_D', 'total_rate', 'feedback'
    )

    # Calculating average total_rate
    average_rating = Evaluation.objects.filter(faculty=faculty).aggregate(avg_rating=Avg('total_rate'))['avg_rating']

    # Convert QuerySet to list of dictionaries
    scores_list = list(scores)

    return JsonResponse({'scores': scores_list, 'average_rating': average_rating}, safe=False)




import json

import re
from textblob import TextBlob
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Evaluation, Faculty
def analyze_feedback(request, faculty_id, subject_id, year, semester):
    # Define the set of offensive words and phrases
    offensive_phrases = {"putang ina", "putangina", "putang ina"}
    offensive_words = {"crap", "idiot", "stupid", "fool", "fuck", "fuck you", "go to hell", "goes to hell",
                       "fuck her", "fuck him", "shit", "bitch", "cunt",
                       "son of a bitch", "dickhead", "tanga", "mulala",
                       "gago", "inutil", "mang mang", "mangmang", "inotil",
                       "bobo"}

    negative_phrases = {"hindi nag tuturo", "hindi pumapasok", "laging late",
                         'mababa mag bigay ','laging galit','pangit','hindi marunong mag turo','masungit','madaling pakisamahan'}

    positive_phrases = {"magaling magturo", "mataas mag bigay", "pogi", "maganda",
                        "mabait", "masipag", "knowledgeable", "cares about students", 
                        "effective teaching", "engaging lectures", "inspiring", 'mahirap pakisamahan'}

    faculty = get_object_or_404(Faculty, id=faculty_id)

    feedback_data = {
        'id': faculty.id_number,
        'name': f'{faculty.first_name} {faculty.last_name}',
        'sentiment': '',
        'average_polarity': 0,
        'average_subjectivity': '',
        'conclusion': '',
        'all_offensive_words': [],  # Changed to list
        'all_negative_phrases': set(),  # Changed to set
        'all_positive_phrases': set()  # Added to store positive phrases
    }

    # Retrieve evaluations associated with the faculty, subject, year, and semester
    evaluations = newEvaluation.objects.filter(
        faculty=faculty,
        subject_id=subject_id,
        year=year,
        semester=semester
    )

    # Initialize variables to store overall sentiment scores
    total_polarity = 0
    total_subjectivity = 0
    num_evaluations = 0

    # Analyze feedback for each evaluation
    for evaluation in evaluations:
        # Preprocess feedback text to remove special characters and ensure case insensitivity
        cleaned_feedback = re.sub(r'[^\w\s]', '', evaluation.feedback.lower())

        # Perform sentiment analysis
        blob = TextBlob(cleaned_feedback)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Check for offensive words and phrases
        detected_offensive_words = set()  # Use a set to store offensive words
        for word in offensive_words:
            if word in cleaned_feedback:
                detected_offensive_words.add(word)

        for phrase in offensive_phrases:
            if phrase in cleaned_feedback:
                detected_offensive_words.add(phrase)

        # Extend the list of all offensive words with the detected words in this feedback
        feedback_data['all_offensive_words'].extend(list(detected_offensive_words))

        # Check for negative phrases
        detected_negative_phrases = set()  # Use a set to store negative phrases
        for phrase in negative_phrases:
            if phrase in cleaned_feedback:
                detected_negative_phrases.add(phrase)

        # Extend the set of all detected negative phrases in this feedback
        feedback_data['all_negative_phrases'].update(detected_negative_phrases)  # Use update instead of extend

        # Check for positive phrases
        detected_positive_phrases = set()  # Use a set to store positive phrases
        for phrase in positive_phrases:
            if phrase in cleaned_feedback:
                detected_positive_phrases.add(phrase)

        # Extend the set of all detected positive phrases in this feedback
        feedback_data['all_positive_phrases'].update(detected_positive_phrases)  # Use update instead of extend

        # Adjust polarity based on the presence of negative or positive phrases
        if detected_negative_phrases:
            polarity -= 0.08
            

        if detected_positive_phrases:
            polarity += 0.08
            

        # Accumulate sentiment scores
        total_polarity += polarity
        total_subjectivity += subjectivity
        num_evaluations += 1

    # Calculate average sentiment scores and determine overall sentiment label
    if num_evaluations > 0:
        average_polarity = total_polarity / num_evaluations
        average_subjectivity = total_subjectivity / num_evaluations

        # Determine sentiment label based on average polarity score
        if average_polarity > 0.3:
            sentiment_label = 'Positive'
            conclusion = "The faculty member is doing an excellent job. Students appreciate their teaching style and find the lectures engaging."
        elif average_polarity < -0.3:
            sentiment_label = 'Negative'
            conclusion = ("The faculty member needs to improve their teaching approach. The faculty member should prioritize improving their teaching approach to address student dissatisfaction with the course materials and delivery. "
                          "This entails revisiting and potentially updating the course materials to ensure they are comprehensive, engaging, and aligned with the learning objectives. "
                          "Additionally, the faculty member should explore varied delivery methods, such as incorporating multimedia resources, interactive activities, and real-world examples to cater to diverse learning styles and enhance student engagement. "
                          "Regular solicitation of feedback from students and willingness to adapt teaching strategies based on their input can also significantly contribute to improving the overall learning experience.")
        else:
            sentiment_label = 'Neutral'
            conclusion = "The result of the sentiment analysis for the faculty evaluation feedback is Neutral, meaning the polarity score might range from -0.3 to +0.3. This indicates that the faculty member is not performing poorly in their teaching approach. However, it is still recommended to improve teaching techniques and methods for better student-teacher relationships."

        # Map the average subjectivity score to subjective or objective
        if average_subjectivity > 0.5:
            subjectivity_label = 'Subjective'
        else:
            subjectivity_label = 'Objective'

        feedback_data['sentiment'] = sentiment_label
        feedback_data['average_polarity'] = average_polarity
        feedback_data['average_subjectivity'] = subjectivity_label
        feedback_data['conclusion'] = conclusion

    else:
        feedback_data['sentiment'] = 'No evaluations found'

    # If sentiment is negative, include only negative phrases
    if feedback_data['sentiment'] == 'Negative':
        feedback_data['all_negative_phrases'] = list(feedback_data['all_negative_phrases'])
        feedback_data.pop('all_positive_phrases')  # Remove 'all_positive_phrases' if sentiment is negative
    else:
        feedback_data.pop('all_negative_phrases')  # Remove 'all_negative_phrases' from feedback_data if sentiment is not negative
        feedback_data['all_positive_phrases'] = list(feedback_data['all_positive_phrases'])  # Convert positive phrases to list

    return JsonResponse({'faculty_feedback': feedback_data})