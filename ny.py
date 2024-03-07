from Departments.models import Subject
from Add_faculty.models import Faculty

# Assuming 'id_number' is the unique identifier for the faculty member
faculty_member = Faculty.objects.get(id_number='19-10264')

# Retrieve the subjects associated with the faculty member
associated_subjects = faculty_member.subjects.all()

# Print or process the associated subjects
for subject in associated_subjects:
    print(subject.description)
