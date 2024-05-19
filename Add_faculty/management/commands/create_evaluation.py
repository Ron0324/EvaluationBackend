from django.core.management.base import BaseCommand
from Add_faculty.models import newEvaluation, Faculty,FacultySubject
from Departments.models import Subject, Semester
from Course_and_Students.models import Student
from decimal import Decimal

class Command(BaseCommand):
    help = 'Manually create new evaluations'

    def handle(self, *args, **kwargs):
        # Input faculty details
        faculty_id = input("Enter Faculty ID: ")

        # Input semester and year
        semester_choice = input("Enter Semester (1 for First, 2 for Second): ")
        year = input("Enter Year: ")

        # Filter faculty subjects by faculty, semester, and year
        faculty_subjects = FacultySubject.objects.filter(
            faculty_id=faculty_id,
            semester=semester_choice,
            year=year
        )

        if not faculty_subjects.exists():
            self.stdout.write(self.style.ERROR(f'Faculty with ID {faculty_id} has no assigned subjects for semester {semester_choice} and year {year}.'))
            return

        # Display the list of subjects to choose from
        self.stdout.write("Subjects for evaluation:")
        for index, faculty_subject in enumerate(faculty_subjects, start=1):
            self.stdout.write(f"{index}. {faculty_subject.subject}")

        # Prompt user to choose a subject
        subject_choice = input("Choose a subject to evaluate (enter number): ")

        try:
            subject_choice = int(subject_choice)
            if subject_choice < 1 or subject_choice > len(faculty_subjects):
                raise ValueError
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid subject choice. Please enter a valid number."))
            return

        selected_faculty_subject = faculty_subjects[subject_choice - 1]

        # Input student ID
        student_id = input("Enter Student ID: ")

        # Validate student ID
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Student with ID {student_id} does not exist.'))
            return

        # Check for existing evaluation
        if newEvaluation.objects.filter(
            student=student,
            subject=selected_faculty_subject.subject,
            semester=semester_choice,
            year=year
        ).exists():
            self.stdout.write(self.style.ERROR(f'The student has already evaluated this subject for semester {semester_choice} and year {year}.'))
            return

        # Input evaluation criteria
        criteria_A = Decimal(input(f"Enter Criteria A score for subject {selected_faculty_subject.subject}: "))
        criteria_B = Decimal(input(f"Enter Criteria B score for subject {selected_faculty_subject.subject}: "))
        criteria_C = Decimal(input(f"Enter Criteria C score for subject {selected_faculty_subject.subject}: "))
        criteria_D = Decimal(input(f"Enter Criteria D score for subject {selected_faculty_subject.subject}: "))
        total_rate = (criteria_A + criteria_B + criteria_C + criteria_D) / 4

        # Input feedback
        feedback = input(f"Enter Feedback for subject {selected_faculty_subject.subject}: ")

        # Create the evaluation entry
        evaluation = newEvaluation.objects.create(
            faculty=selected_faculty_subject.faculty,
            student=student,
            subject=selected_faculty_subject.subject,
            semester=semester_choice,
            year=year,
            criteria_A=criteria_A,
            criteria_B=criteria_B,
            criteria_C=criteria_C,
            criteria_D=criteria_D,
            total_rate=total_rate,
            feedback=feedback
        )

        # Display the created evaluation
        self.stdout.write(self.style.SUCCESS(f'Successfully created new evaluation: {evaluation}'))