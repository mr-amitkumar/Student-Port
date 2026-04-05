from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import date, timedelta
from .models import Student, FeePayment, Attendance, Notice
from .forms import (CustomLoginForm, CustomRegisterForm, StudentForm,
                    FeePaymentForm, AttendanceForm, NoticeForm)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect('dashboard')
    return render(request, 'portal/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CustomRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome.')
        return redirect('dashboard')
    return render(request, 'portal/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today, status='present').values('student').distinct().count()
    absent_today = Attendance.objects.filter(date=today, status='absent').values('student').distinct().count()
    pending_fees = FeePayment.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    collected_fees = FeePayment.objects.filter(status='paid').aggregate(total=Sum('paid_amount'))['total'] or 0
    recent_students = Student.objects.order_by('-created_at')[:5]
    recent_fees = FeePayment.objects.order_by('-created_at')[:5]
    notices = Notice.objects.filter(is_active=True)[:3]
    dept_stats = Student.objects.values('department').annotate(count=Count('id')).order_by('-count')[:5]

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'pending_fees': pending_fees,
        'collected_fees': collected_fees,
        'recent_students': recent_students,
        'recent_fees': recent_fees,
        'notices': notices,
        'dept_stats': dept_stats,
        'today': today,
    }
    return render(request, 'portal/dashboard.html', context)


# ─── STUDENT VIEWS ───────────────────────────────────────────────────────────

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    status = request.GET.get('status', '')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(student_id__icontains=query) | Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    if dept:
        students = students.filter(department__icontains=dept)
    if status:
        students = students.filter(status=status)
    departments = Student.objects.values_list('department', flat=True).distinct()
    return render(request, 'portal/student_list.html', {
        'students': students, 'query': query, 'departments': departments,
        'selected_dept': dept, 'selected_status': status,
    })


@login_required
def student_add(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.added_by = request.user
        student.save()
        messages.success(request, f'Student {student.full_name()} added successfully!')
        return redirect('student_list')
    return render(request, 'portal/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Student {student.full_name()} updated!')
        return redirect('student_detail', pk=pk)
    return render(request, 'portal/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name()
        student.delete()
        messages.success(request, f'Student {name} deleted.')
        return redirect('student_list')
    return render(request, 'portal/confirm_delete.html', {'object': student, 'type': 'Student'})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    fees = student.fees.all().order_by('-created_at')
    attendances = student.attendances.all().order_by('-date')[:30]
    total_fee = fees.aggregate(total=Sum('amount'))['total'] or 0
    paid_fee = fees.filter(status='paid').aggregate(total=Sum('paid_amount'))['total'] or 0
    total_days = attendances.count()
    present_days = student.attendances.filter(status='present').count()
    attendance_pct = round((present_days / total_days * 100) if total_days > 0 else 0, 1)
    return render(request, 'portal/student_detail.html', {
        'student': student, 'fees': fees, 'attendances': attendances,
        'total_fee': total_fee, 'paid_fee': paid_fee,
        'attendance_pct': attendance_pct, 'present_days': present_days, 'total_days': total_days,
    })


# ─── FEE VIEWS ───────────────────────────────────────────────────────────────

@login_required
def fee_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    fees = FeePayment.objects.select_related('student').all()
    if query:
        fees = fees.filter(
            Q(student__first_name__icontains=query) | Q(student__last_name__icontains=query) |
            Q(student__student_id__icontains=query) | Q(transaction_id__icontains=query)
        )
    if status:
        fees = fees.filter(status=status)
    total_collected = fees.filter(status='paid').aggregate(t=Sum('paid_amount'))['t'] or 0
    total_pending = fees.filter(status='pending').aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'portal/fee_list.html', {
        'fees': fees, 'query': query, 'selected_status': status,
        'total_collected': total_collected, 'total_pending': total_pending,
    })


@login_required
def fee_add(request):
    form = FeePaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        fee = form.save(commit=False)
        fee.recorded_by = request.user
        fee.save()
        messages.success(request, 'Fee record added successfully!')
        return redirect('fee_list')
    return render(request, 'portal/fee_form.html', {'form': form, 'title': 'Add Fee Record'})


@login_required
def fee_edit(request, pk):
    fee = get_object_or_404(FeePayment, pk=pk)
    form = FeePaymentForm(request.POST or None, instance=fee)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fee record updated!')
        return redirect('fee_list')
    return render(request, 'portal/fee_form.html', {'form': form, 'title': 'Edit Fee Record', 'fee': fee})


@login_required
def fee_delete(request, pk):
    fee = get_object_or_404(FeePayment, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee record deleted.')
        return redirect('fee_list')
    return render(request, 'portal/confirm_delete.html', {'object': fee, 'type': 'Fee Record'})


# ─── ATTENDANCE VIEWS ─────────────────────────────────────────────────────────

@login_required
def attendance_list(request):
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    status = request.GET.get('status', '')
    attendances = Attendance.objects.select_related('student').all()
    if query:
        attendances = attendances.filter(
            Q(student__first_name__icontains=query) | Q(student__last_name__icontains=query) |
            Q(subject__icontains=query)
        )
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    if status:
        attendances = attendances.filter(status=status)
    return render(request, 'portal/attendance_list.html', {
        'attendances': attendances, 'query': query,
        'selected_date': date_filter, 'selected_status': status,
    })


@login_required
def attendance_mark(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        att = form.save(commit=False)
        att.marked_by = request.user
        att.save()
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_list')
    return render(request, 'portal/attendance_form.html', {'form': form, 'title': 'Mark Attendance'})


@login_required
def attendance_edit(request, pk):
    att = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=att)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Attendance updated!')
        return redirect('attendance_list')
    return render(request, 'portal/attendance_form.html', {'form': form, 'title': 'Edit Attendance', 'att': att})


@login_required
def attendance_delete(request, pk):
    att = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        att.delete()
        messages.success(request, 'Attendance record deleted.')
        return redirect('attendance_list')
    return render(request, 'portal/confirm_delete.html', {'object': att, 'type': 'Attendance Record'})


# ─── NOTICE VIEWS ─────────────────────────────────────────────────────────────

@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'portal/notice_list.html', {'notices': notices})


@login_required
def notice_add(request):
    form = NoticeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        notice = form.save(commit=False)
        notice.posted_by = request.user
        notice.save()
        messages.success(request, 'Notice posted!')
        return redirect('notice_list')
    return render(request, 'portal/notice_form.html', {'form': form, 'title': 'Post Notice'})


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted.')
        return redirect('notice_list')
    return render(request, 'portal/confirm_delete.html', {'object': notice, 'type': 'Notice'})
