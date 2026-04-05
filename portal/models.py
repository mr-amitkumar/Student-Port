from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated')]

    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField(default=1)
    roll_number = models.CharField(max_length=20, blank=True)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']


class FeePayment(models.Model):
    FEE_TYPE_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('exam', 'Exam Fee'),
        ('library', 'Library Fee'),
        ('hostel', 'Hostel Fee'),
        ('transport', 'Transport Fee'),
        ('miscellaneous', 'Miscellaneous'),
    ]
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('waived', 'Waived'),
    ]
    PAYMENT_MODE = [
        ('cash', 'Cash'),
        ('online', 'Online Transfer'),
        ('cheque', 'Cheque'),
        ('dd', 'Demand Draft'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=30, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    semester = models.IntegerField(default=1)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.fee_type} - {self.status}"

    def balance(self):
        return self.amount - self.paid_amount

    class Meta:
        ordering = ['-created_at']


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'date', 'subject']


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
