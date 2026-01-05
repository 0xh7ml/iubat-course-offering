from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = "tb_departments"
    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Semester(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"
        db_table = "tb_semesters"

    def __str__(self):
        return self.name
    
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credits = models.IntegerField()
    lab_course = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "tb_courses"

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class CourseSchedule(models.Model):
    DAY_CHOICES = [
        ('1', 'Saturday'),
        ('2', 'Sunday'),
        ('3', 'Monday'),
        ('4', 'Tuesday'),
        ('5', 'Wednesday'),
        ('6', 'Thursday'),
        ('7', 'Friday'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=9, choices=DAY_CHOICES)
    time_slot = models.CharField(max_length=50)
    section = models.CharField(max_length=2)
    room_no = models.CharField(max_length=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course Schedule"
        verbose_name_plural = "Course Schedules"
        db_table = "tb_course_schedules"
        unique_together = ('course', 'day', 'time_slot', 'section')
    
    def __str__(self):
        return f"{self.course.course_code} - {self.day} {self.time_slot} (Section {self.section})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_id = models.CharField(max_length=8, unique=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        db_table = "tb_students"

    def __str__(self):
        return f"{self.student_id} - {self.student_name}"
    

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')
    year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        db_table = "tb_enrollments"
        unique_together = ('student', 'course', 'semester', 'year')

    def __str__(self):
        return f"{self.student.student_id} enrolled in {self.course.course_code} for {self.semester} {self.year}"