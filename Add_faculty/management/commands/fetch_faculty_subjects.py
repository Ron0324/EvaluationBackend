from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.http.response import JsonResponse
from Add_faculty.models import Faculty, FacultySubject

class Command(BaseCommand):
    help = 'Fetch subjects associated with a faculty member for a given year and semester'

    def add_arguments(self, parser):
        parser.add_argument('faculty_id', type=int, help='Faculty ID')
        parser.add_argument('year', type=int, help='Year')
        parser.add_argument('semester', type=int, help='Semester')

    def handle(self, *args, **kwargs):
        faculty_id = kwargs['faculty_id']
        year = kwargs['year']
        semester = kwargs['semester']

        try:
            # Simulate the view function logic
            faculty = get_object_or_404(Faculty, id=faculty_id)
            semester = int(semester)
            if semester not in [1, 2]:
                self.stdout.write(self.style.ERROR('Invalid semester value'))
                return
            
            faculty_subjects = FacultySubject.objects.filter(faculty=faculty, year=year, semester=semester)
            subjects = [faculty_subject.subject.Subname for faculty_subject in faculty_subjects]

            self.stdout.write(self.style.SUCCESS('Subjects associated with faculty ID {}:'.format(faculty_id)))
            for subject in subjects:
                self.stdout.write(self.style.SUCCESS('- {}'.format(subject)))
        except Faculty.DoesNotExist:
            raise CommandError('Faculty not found')