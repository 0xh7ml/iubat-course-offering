from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from offering.models import Department, Semester, Course, CourseSchedule, Student

class Command(BaseCommand):
    help = 'Create sample data for testing the student portal'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create Departments
        cse_dept = Department.objects.get_or_create(
            code='CSE',
            defaults={'name': 'Computer Science and Engineering', 'status': True}
        )[0]
        
        eee_dept = Department.objects.get_or_create(
            code='EEE',
            defaults={'name': 'Electrical and Electronic Engineering', 'status': True}
        )[0]

        # Create Semester
        semester = Semester.objects.get_or_create(
            name='Fall 2026',
            defaults={}
        )[0]

        # Create Courses
        courses_data = [
            {'code': 'CSE101', 'name': 'Introduction to Programming', 'dept': cse_dept, 'credits': 3, 'lab': False},
            {'code': 'CSE102', 'name': 'Programming Lab', 'dept': cse_dept, 'credits': 1, 'lab': True},
            {'code': 'CSE201', 'name': 'Data Structures', 'dept': cse_dept, 'credits': 3, 'lab': False},
            {'code': 'CSE202', 'name': 'Data Structures Lab', 'dept': cse_dept, 'credits': 1, 'lab': True},
            {'code': 'CSE301', 'name': 'Database Management System', 'dept': cse_dept, 'credits': 3, 'lab': False},
            {'code': 'CSE302', 'name': 'Database Lab', 'dept': cse_dept, 'credits': 1, 'lab': True},
            {'code': 'EEE101', 'name': 'Circuit Analysis', 'dept': eee_dept, 'credits': 3, 'lab': False},
            {'code': 'EEE102', 'name': 'Circuit Lab', 'dept': eee_dept, 'credits': 1, 'lab': True},
        ]

        courses = {}
        for course_data in courses_data:
            course = Course.objects.get_or_create(
                course_code=course_data['code'],
                defaults={
                    'course_name': course_data['name'],
                    'department': course_data['dept'],
                    'credits': course_data['credits'],
                    'lab_course': course_data['lab']
                }
            )[0]
            courses[course_data['code']] = course

        # Create Course Schedules
        schedules_data = [
            {'course': 'CSE101', 'day': '1', 'time': '08:00 AM - 09:30 AM', 'section': 'A', 'room': '101'},
            {'course': 'CSE101', 'day': '3', 'time': '08:00 AM - 09:30 AM', 'section': 'A', 'room': '101'},
            {'course': 'CSE102', 'day': '2', 'time': '10:00 AM - 12:00 PM', 'section': 'A', 'room': '201'},
            {'course': 'CSE201', 'day': '1', 'time': '10:00 AM - 11:30 AM', 'section': 'A', 'room': '102'},
            {'course': 'CSE201', 'day': '4', 'time': '10:00 AM - 11:30 AM', 'section': 'A', 'room': '102'},
            {'course': 'CSE202', 'day': '3', 'time': '02:00 PM - 04:00 PM', 'section': 'A', 'room': '202'},
            {'course': 'CSE301', 'day': '2', 'time': '08:00 AM - 09:30 AM', 'section': 'A', 'room': '103'},
            {'course': 'CSE301', 'day': '5', 'time': '08:00 AM - 09:30 AM', 'section': 'A', 'room': '103'},
            {'course': 'CSE302', 'day': '4', 'time': '02:00 PM - 04:00 PM', 'section': 'A', 'room': '203'},
            {'course': 'EEE101', 'day': '1', 'time': '02:00 PM - 03:30 PM', 'section': 'A', 'room': '301'},
            {'course': 'EEE101', 'day': '3', 'time': '02:00 PM - 03:30 PM', 'section': 'A', 'room': '301'},
            {'course': 'EEE102', 'day': '2', 'time': '02:00 PM - 04:00 PM', 'section': 'A', 'room': '401'},
        ]

        for schedule_data in schedules_data:
            CourseSchedule.objects.get_or_create(
                course=courses[schedule_data['course']],
                day=schedule_data['day'],
                time_slot=schedule_data['time'],
                section=schedule_data['section'],
                defaults={'room_no': schedule_data['room']}
            )

        # Create Test Students
        students_data = [
            {'id': '12345678', 'name': 'John Doe', 'email': 'john.doe@student.iubat.edu', 'dept': cse_dept},
            {'id': '23456789', 'name': 'Jane Smith', 'email': 'jane.smith@student.iubat.edu', 'dept': cse_dept},
            {'id': '34567890', 'name': 'Bob Johnson', 'email': 'bob.johnson@student.iubat.edu', 'dept': eee_dept},
        ]

        # Default password: "student123"
        default_password = "student123"

        for student_data in students_data:
            # Create or get Django user
            user, user_created = User.objects.get_or_create(
                username=student_data['id'],
                defaults={
                    'email': student_data['email'],
                    'first_name': student_data['name'].split()[0],
                    'last_name': ' '.join(student_data['name'].split()[1:]) if len(student_data['name'].split()) > 1 else '',
                }
            )
            
            if user_created:
                user.set_password(default_password)
                user.save()
            
            # Create or get student profile
            student, student_created = Student.objects.get_or_create(
                student_id=student_data['id'],
                defaults={
                    'user': user,
                    'student_name': student_data['name'],
                    'student_email': student_data['email'],
                    'department': student_data['dept'],
                    'is_verified': True
                }
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Test students (password: student123):')
        for student_data in students_data:
            self.stdout.write(f'  - ID: {student_data["id"]}, Name: {student_data["name"]}')