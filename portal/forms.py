from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, FeePayment, Attendance, Notice


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Password'
    }))


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['added_by', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'student_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. STU2024001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'course': forms.TextInput(attrs={'class': 'form-input'}),
            'department': forms.TextInput(attrs={'class': 'form-input'}),
            'semester': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 12}),
            'roll_number': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        exclude = ['recorded_by', 'created_at']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-input'}),
            'fee_type': forms.Select(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'paid_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'payment_mode': forms.Select(attrs={'class': 'form-input'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'semester': forms.NumberInput(attrs={'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ['marked_by', 'created_at']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }
