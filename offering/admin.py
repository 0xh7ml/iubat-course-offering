from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Department, Semester, Course, CourseSchedule, Student, Enrollment

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'code')
    list_editable = ('status',)
    ordering = ('code',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Department Information', {
            'fields': ('code', 'name', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Semester Information', {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'credits', 'lab_course', 'created_at')
    list_filter = ('department', 'lab_course', 'credits', 'created_at')
    search_fields = ('course_name', 'course_code')
    list_editable = ('lab_course',)
    ordering = ('course_code',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_code', 'course_name', 'department', 'credits', 'lab_course')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_course_code', 'get_course_name', 'get_day_display', 'time_slot', 'section', 'room_no')
    list_filter = ('day', 'course__department', 'section', 'created_at')
    search_fields = ('course__course_code', 'course__course_name', 'time_slot', 'section', 'room_no')
    list_editable = ('time_slot', 'section', 'room_no')
    ordering = ('course__course_code', 'day', 'time_slot', 'section')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['course']
    
    def get_course_code(self, obj):
        return obj.course.course_code
    get_course_code.short_description = 'Course Code'
    get_course_code.admin_order_field = 'course__course_code'
    
    def get_course_name(self, obj):
        return obj.course.course_name
    get_course_name.short_description = 'Course Name'
    get_course_name.admin_order_field = 'course__course_name'
    
    def get_day_display(self, obj):
        return obj.get_day_display()
    get_day_display.short_description = 'Day'
    get_day_display.admin_order_field = 'day'
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('course', 'day', 'time_slot', 'section', 'room_no')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'student_email', 'department', 'is_verified', 'get_username', 'created_at')
    list_filter = ('department', 'is_verified', 'created_at')
    search_fields = ('student_id', 'student_name', 'student_email', 'user__username')
    list_editable = ('is_verified',)
    ordering = ('student_id',)
    
    def get_username(self, obj):
        return obj.user.username if obj.user else 'No User'
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new student
            # Validate that email is provided
            if not obj.student_email:
                messages.error(request, 'Email address is required to create a user account.')
                return
                
            # Create Django User
            if not obj.user_id:
                # Generate default password (student can change later)
                default_password = 'student123'  # You can make this more secure
                
                try:
                    # Check if user with this email already exists
                    if User.objects.filter(email=obj.student_email).exists():
                        messages.error(request, f'A user with email {obj.student_email} already exists.')
                        return
                        
                    user = User.objects.create_user(
                        username=obj.student_id,
                        email=obj.student_email,
                        password=default_password,
                        first_name=obj.student_name.split()[0] if obj.student_name else '',
                        last_name=' '.join(obj.student_name.split()[1:]) if len(obj.student_name.split()) > 1 else ''
                    )
                    obj.user = user
                    messages.success(request, f'User created with username: {obj.student_id}, email: {obj.student_email} and password: {default_password}')
                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return
        
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_id', 'student_name', 'student_email', 'department', 'is_verified'),
            'description': 'The email address will be used for the Django user account.'
        }),
        ('User Account', {
            'fields': ('user',),
            'classes': ('collapse',),
            'description': 'Django user account is auto-created when student is saved.'
        })
    )
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('get_student_id', 'get_student_name', 'course', 'semester', 'year', 'created_at')
    list_filter = ('semester', 'year', 'course__department', 'created_at')
    search_fields = ('student__student_id', 'student__student_name', 'course__course_code', 'course__course_name')
    ordering = ('-year', 'semester', 'student__student_id')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['student', 'course']
    
    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'
    get_student_id.admin_order_field = 'student__student_id'
    
    def get_student_name(self, obj):
        return obj.student.student_name
    get_student_name.short_description = 'Student Name'
    get_student_name.admin_order_field = 'student__student_name'
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course', 'semester', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
