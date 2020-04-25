from django.urls import path
from library import views
#from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.HomeView.as_view(), name='home'),
    #path('adminpage/', views.create_user, name='create_user'),
    path('adminpage/', views.CreateUserView.as_view(), name='create_user'),
    
    path('create-student/(?P<username>[\w.@+-]+)/(?P<admin>[\w.@+-]+)', views.CreateStudentView.as_view(), name='create_student'),
    #path('create-student/(?P<username>[\w.@+-]+)/(?P<admin>[\w.@+-]+)', views.create_student, name='create_student'),
    path('create-staff/(?P<username>[\w.@+-]+)/(?P<admin>[\w.@+-]+)', views.create_staff, name='create_staff'),    
    path('ajax/change_request_issue/', views.change_request_issue, name='change_request_issue'),
    path('student-dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    
    path('ajax/change_issue_status/', views.change_issue_status, name='change_issue_status'),
    path('staff-issue/', views.staff_issue, name='staff_dashboard'),
    path('staff-addbook/', views.staff_addbook, name='staff_addbook'),
    path('logout/',views.logout_view),
    
]
