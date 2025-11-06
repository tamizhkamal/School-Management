from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='members'),
    path('home_page', views.home_page, name='home_page'),
    path('topics_detail', views.topics_detail, name='topics_detail'),
    path('topics_list', views.topics_list, name='topics_list'),
    path('contact', views.contact, name='contact'),

    # admin
    path('login_view', views.login_view, name='login_view'),
    path('admin-dashboard', views.admin_dash, name='admin_dash'),
    path('student-management', views.Student_create, name='Student_create'),
    path('mark-management', views.Mark_Management, name='Mark_Management'),
    path('Addendance-Management', views.Addendance_Management, name='Addendance_Management'),
    path('Students-list', views.Student_list, name='Student_list'),
    path('Students-details/<student_id>', views.Student_details, name='Student_details'),
    path('logout_view', views.logout_view, name='logout_view'),
    path("export-marks/", views.export_marks, name="export_marks"),
    # path('attendance/', views.attendance_view, name='attendance'),
    # path('attendance/', views.student_attendance_list, name='student_attendance_list'),

    path('import-marks/', views.import_marks_from_excel_view, name='import_marks'),
    path('import-students/', views.import_student_from_excel_view, name='import_students'),
    path('import-attendance/', views.import_attendance_from_excel_view, name='import_students'),


    ]
