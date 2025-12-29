from django.contrib import admin
from .models import Department, Semester, Course, Student, StudentResult, Enrollment

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


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'student_email', 'department', 'is_verified', 'created_at')
    list_filter = ('department', 'is_verified', 'created_at')
    search_fields = ('student_id', 'student_name', 'student_email')
    list_editable = ('is_verified',)
    ordering = ('student_id',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_id', 'student_name', 'student_email', 'department', 'is_verified')
        }),
        ('Authentication', {
            'fields': ('student_password',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_student_id', 'status', 'cgpa', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__student_id', 'student__student_name')
    list_editable = ('status', 'cgpa')
    ordering = ('-cgpa',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'
    get_student_id.admin_order_field = 'student__student_id'
    
    fieldsets = (
        ('Student Result Information', {
            'fields': ('student', 'status', 'cgpa')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
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
