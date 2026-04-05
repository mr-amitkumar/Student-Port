from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Fees
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/add/', views.fee_add, name='fee_add'),
    path('fees/<int:pk>/edit/', views.fee_edit, name='fee_edit'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    # Notices
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.notice_add, name='notice_add'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
]
