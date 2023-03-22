from django.urls import path
from .views import (register,user_login,add_student,dashboard,user_logout,view_student_list,add_teacher,
                    add_department,view_department_list,view_teacher_list,
                    add_student_excel,admin_dashboard,student_dashboard)

app_name ='stakeholder'
urlpatterns = [
    path('register/',register,name="register"),
    path('login/',user_login,name="login"), 
    path('logout/',user_logout,name="logout"),
    path('dashboard/',dashboard,name="dashboard"),
    path('institution/admin/dashboard/',admin_dashboard,name="admin-dashboard"),
    path('institution/student/dashboard/',student_dashboard,name="student-dashboard"),
    path('institution/add_student/',add_student,name="add-student"),
    path('institution/admin/add_student_excel/',add_student_excel,name="add-student-excel"),
    path('institution/student_list/',view_student_list,name="student-list"),
    path('institution/add_teacher/',add_teacher,name="add-teacher"),
    path('institution/teacher_list/',view_teacher_list,name="teacher-list"),
    path('institution/add_department/',add_department,name="add-department"),
    path('institution/department_list/',view_department_list,name="department-list"),
]