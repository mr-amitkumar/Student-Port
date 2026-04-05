from django.contrib import admin
from .models import Student, FeePayment, Attendance, Notice

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'course', 'department', 'semester', 'status']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    list_filter = ['status', 'department', 'semester']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount', 'paid_amount', 'status', 'due_date']
    list_filter = ['status', 'fee_type']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'subject', 'status']
    list_filter = ['status', 'date']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'created_at', 'is_active']
