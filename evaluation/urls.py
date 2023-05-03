from django.urls import path
from .views import (factor_list,start_evaluation,course_evaluation,course_evaluation_form,course_evaluation_save,
                    colleague_evaluation,colleague_evaluation_form,colleague_evaluation_save,course_evaluation_parent,
                    course_evaluation_form_parent,course_evaluation_parent_save,teacher_evaluation_administrations,
                    teacher_evaluation_administration_form,teacher_evaluation_administration_save,self_evaluation_form,
                    self_evaluation_save,
                    current_evaluation_report_view,student_evaluation_report,colleague_evaluation_report,parent_evaluation_report,
                    administrator_evaluation_report,self_evaluation_report)
               
app_name ='evaluation'
urlpatterns = [
    path('institution/factors',factor_list,name='factor-list'),
    path('institution/start-evaluation',start_evaluation,name='start-evaluation'),
    path('institution/<int:c_id>/evaluation-form',course_evaluation_form,name='course-evaluation-form'),
    path('institution/course-evaluation/',course_evaluation,name='course-evaluation'),
    path('institution/course-evaluation-save/<int:c_id>/<int:e_id>',course_evaluation_save,name='course-evaluation-save'),

    path('institution/colleague-evaluation/',colleague_evaluation,name='colleague-evaluation'),
    path('institution/<int:t_id>/colleague-evaluation-form',colleague_evaluation_form,name='colleague-evaluation-form'),
    path('institution/colleague-evaluation-save/<int:t_id>/<int:e_id>',colleague_evaluation_save,name='colleague-evaluation-save'),

    path('institution/course-evaluation-parent/',course_evaluation_parent,name='course-evaluation-parent'),
    path('institution/<int:c_id>/evaluation-form-parent',course_evaluation_form_parent,name='course-evaluation-form-parent'),
    path('institution/course-evaluation-save-parent/<int:c_id>/<int:e_id>',course_evaluation_parent_save,name='course-evaluation-parent-save'),


    path('institution/teacher-evaluation-administrator/',teacher_evaluation_administrations,name='teacher-evaluation-administrator'),
    path('institution/<int:t_id>/teacher-evaluation-form-administrator',teacher_evaluation_administration_form,name='teacher-evaluation-form-administrator'),
    path('institution/teacher-evaluation-administrator-save/<int:t_id>/<int:e_id>',teacher_evaluation_administration_save,name='teacher-evaluation-administrator-save'),


    path('institution/self-evaluation-form',self_evaluation_form,name='self-evaluation-form'),
    path('institution/self-evaluation-save/<int:e_id>',self_evaluation_save,name='self-evaluation-save'),

    path('institution/current-evaluation-report',current_evaluation_report_view,name='current-evaluation-report'),
    path('institution/student-evaluation-report/<int:e_id>',student_evaluation_report,name='student-evaluation-report'),

    path('institution/colleague-evaluation-report/<int:e_id>',colleague_evaluation_report,name='colleague-evaluation-report'),
    path('institution/parent-evaluation-report/<int:e_id>',parent_evaluation_report,name='parent-evaluation-report'),
    path('institution/administrator-evaluation-report/<int:e_id>',administrator_evaluation_report,name='administrator-evaluation-report'),
    path('institution/self-evaluation-report/<int:e_id>',self_evaluation_report,name='self-evaluation-report'),


]
