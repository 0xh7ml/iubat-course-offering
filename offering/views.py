from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from datetime import datetime
from .models import Student, Course, CourseSchedule, Enrollment, Semester, Department

# Home view - redirect to student login
def home(request):
    """Home view redirects to student login"""
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')
    return redirect('student_login')

# Student Authentication Views
def student_login(request):
    """Student login view using Django authentication"""
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        if student_id and password:
            # Authenticate using student_id as username
            user = authenticate(request, username=student_id, password=password)
            
            if user is not None:
                # Check if user has a student profile
                try:
                    student = user.student_profile
                    if student.is_verified:
                        login(request, user)
                        messages.success(request, f'Welcome back, {student.student_name}!')
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, 'Your account is not verified yet. Please contact administration.')
                except Student.DoesNotExist:
                    messages.error(request, 'This account is not associated with a student profile.')
            else:
                messages.error(request, 'Invalid student ID or password.')
        else:
            messages.error(request, 'Please provide both student ID and password.')
    
    return render(request, 'auth/login.html')

def student_logout(request):
    """Student logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student_login')



@login_required(login_url='student_login')
def student_dashboard(request):
    """Student dashboard with info cards"""
    student = request.user.student_profile
    
    # Get student statistics
    total_enrollments = Enrollment.objects.filter(student=student).count()
    current_semester = Semester.objects.first()  # You may want to add logic to get current semester
    current_year = datetime.now().year
    current_enrollments = Enrollment.objects.filter(
        student=student, 
        semester=current_semester, 
        year=current_year
    ).count() if current_semester else 0
    
    context = {
        'student': student,
        'total_enrollments': total_enrollments,
        'current_enrollments': current_enrollments,
        'current_semester': current_semester,
    }
    return render(request, 'student/dashboard.html', context)

@login_required(login_url='student_login')
def course_enrollment(request):
    """Course enrollment view showing available courses"""
    student = request.user.student_profile
    
    # Get current semester and year
    current_semester = Semester.objects.first()
    current_year = datetime.now().year
    
    # Get all available course schedules
    course_schedules = CourseSchedule.objects.select_related('course', 'course__department').all()
    
    # Get already enrolled courses for current semester
    enrolled_courses = Enrollment.objects.filter(
        student=student,
        semester=current_semester,
        year=current_year
    ).values_list('course_id', flat=True) if current_semester else []
    
    # Handle enrollment
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        action = request.POST.get('action', 'enroll')
        
        if course_id and current_semester:
            try:
                with transaction.atomic():
                    course = get_object_or_404(Course, id=course_id)
                    
                    if action == 'enroll':
                        # Check if already enrolled
                        if not Enrollment.objects.filter(
                            student=student,
                            course=course,
                            semester=current_semester,
                            year=current_year
                        ).exists():
                            
                            Enrollment.objects.create(
                                student=student,
                                course=course,
                                semester=current_semester,
                                year=current_year
                            )
                            messages.success(request, f'Successfully enrolled in {course.course_code} - {course.course_name}')
                        else:
                            messages.warning(request, f'You are already enrolled in {course.course_code}')
                    
                    elif action == 'unenroll':
                        # Remove enrollment
                        enrollment = Enrollment.objects.filter(
                            student=student,
                            course=course,
                            semester=current_semester,
                            year=current_year
                        ).first()
                        
                        if enrollment:
                            enrollment.delete()
                            messages.success(request, f'Successfully unenrolled from {course.course_code} - {course.course_name}')
                        else:
                            messages.warning(request, f'You are not enrolled in {course.course_code}')
                    
                    return redirect('course_enrollment')
                        
            except Exception as e:
                messages.error(request, 'An error occurred during the operation. Please try again.')
        else:
            messages.error(request, 'Invalid course selection or no active semester.')
    
    context = {
        'student': student,
        'course_schedules': course_schedules,
        'enrolled_courses': list(enrolled_courses),
        'current_semester': current_semester,
        'current_year': current_year,
    }
    return render(request, 'student/course_enrollment.html', context)

@login_required(login_url='student_login')
def student_routine(request):
    """Student routine view showing weekly schedule"""
    student = request.user.student_profile
    
    # Get current semester and year
    current_semester = Semester.objects.first()
    current_year = datetime.now().year
    
    # Get enrolled courses for current semester
    enrolled_courses = []
    routine_data = {}
    
    if current_semester:
        enrollments = Enrollment.objects.filter(
            student=student,
            semester=current_semester,
            year=current_year
        ).select_related('course')
        
        enrolled_course_ids = [e.course.id for e in enrollments]
        enrolled_courses = [e.course for e in enrollments]
        
        # Get course schedules for enrolled courses
        schedules = CourseSchedule.objects.filter(
            course_id__in=enrolled_course_ids
        ).select_related('course').order_by('day', 'time_slot')
        
        # Organize by day
        days = ['1', '2', '3', '4', '5', '6', '7']  # Saturday to Friday
        day_names = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for i, day in enumerate(days):
            day_schedules = schedules.filter(day=day).order_by('time_slot')
            routine_data[day_names[i]] = day_schedules
    
    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'routine_data': routine_data,
        'current_semester': current_semester,
        'current_year': current_year,
    }
    return render(request, 'student/routine.html', context)

# AJAX endpoint for quick enrollment
@login_required(login_url='student_login')
def ajax_enroll_course(request):
    """AJAX endpoint for course enrollment"""
    if request.method == 'POST':
        student = request.user.student_profile
        
        course_id = request.POST.get('course_id')
        current_semester = Semester.objects.first()
        current_year = datetime.now().year
        
        if course_id and current_semester:
            try:
                with transaction.atomic():
                    course = get_object_or_404(Course, id=course_id)
                    
                    # Check if already enrolled
                    if not Enrollment.objects.filter(
                        student=student,
                        course=course,
                        semester=current_semester,
                        year=current_year
                    ).exists():
                        
                        Enrollment.objects.create(
                            student=student,
                            course=course,
                            semester=current_semester,
                            year=current_year
                        )
                        return JsonResponse({
                            'success': True,
                            'message': f'Successfully enrolled in {course.course_code}'
                        })
                    else:
                        return JsonResponse({
                            'success': False,
                            'message': f'Already enrolled in {course.course_code}'
                        })
                        
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'An error occurred during enrollment'
                })
        
        return JsonResponse({
            'success': False,
            'message': 'Invalid course selection'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
