from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from stakeholder.models import Institution,Student,Parent,Department,Teacher,Course,Administrator
from .models import Factor,StakeholderTag,Question,InstitutionTag,EvaluationEvent,StudentEvaluationResponse,TeacherEvaluationResponse, ParentEvaluationResponse, AdministrationEvaluationResponse, SelfEvaluationResponse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
import itertools
import plotly.graph_objs as go
from plotly.offline import plot
# Create your views here.


def factor_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            factors = Factor.objects.filter(institution=institution[0])
            context={
                "factors" : factors,
                'admin' : institution[0].institution_admin,
            }
            return render(request,'factor_list.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')


def start_evaluation(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            factors = Factor.objects.filter(institution=institution)
            #creating factors for institutions
            stakeholder_tag = StakeholderTag.objects.all()
            institution_tag = InstitutionTag.objects.all()

            #stakeholders
            student = stakeholder_tag[0]
            teacher = stakeholder_tag[1]
            self = stakeholder_tag[2]
            parent = stakeholder_tag[3]
            administrator = stakeholder_tag[4]

            #institutions
            primary = institution_tag[0]
            secondary = institution_tag[1]
            tertiary = institution_tag[2]


            if request.method == "POST":

                does_ongoing_evaluation_exists = EvaluationEvent.objects.filter(Q(institution = institution) & Q(is_start = True) & Q(is_end = False)).exists()

                if does_ongoing_evaluation_exists:
                    return HttpResponse("There is an ongoing evaluation")
                else:
                    stakeholders = request.POST.getlist('stakeholder')

                    student_factors = request.POST.getlist('student_factors')
                    teacher_factors = request.POST.getlist('teacher_factors')
                    parent_factors = request.POST.getlist('parent_factors')
                    self_factors = request.POST.getlist('self_factors')
                    administrator_factors = request.POST.getlist('administrator_factors')
                    
                    start_date = request.POST.get('start_date')
                    end_date = request.POST.get('end_date')

                    evaluation_event = EvaluationEvent(institution = institution,start_date = start_date, end_date = end_date,is_start = True)
                    evaluation_event.save()
                    with transaction.atomic():
                        for id in stakeholders:
                            stakeholder = StakeholderTag.objects.get(id=id)
                            evaluation_event.stakeholder_tag.add(stakeholder)

                        for id in student_factors:
                            factor = Factor.objects.get(id=id)
                            evaluation_event.student_factor.add(factor)
                        
                        for id in teacher_factors:
                            factor = Factor.objects.get(id=id)
                            evaluation_event.teacher_factor.add(factor)
                        
                        for id in parent_factors:
                            factor = Factor.objects.get(id=id)
                            evaluation_event.parent_factor.add(factor)
                        
                        for id in self_factors:
                            factor = Factor.objects.get(id=id)
                            evaluation_event.self_factor.add(factor)
                        
                        for id in administrator_factors:
                            factor = Factor.objects.get(id=id)
                            evaluation_event.administrator_factor.add(factor)
                        
                    return redirect("evaluation:start-evaluation")

            if request.method == "GET":
                context={
                    "factors" : factors,
                    "student" : student,
                    "teacher" : teacher,
                    "self" : self,
                    "administrator" : administrator,
                    "parent" : parent,

                    "primary" : primary,
                    "secondary" : secondary,
                    "tertiary" : tertiary,
                    
                    'admin' : institution.institution_admin,
                    'institution': institution,
                }
            
                return render(request, 'create_evaluation.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    

def course_evaluation(request):
    if request.user.is_authenticated:
        now = timezone.now()
        student = Student.objects.filter(user = request.user).first()
        if student:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = student.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    evaluated_courses = Course.objects.filter(
                        Q(studentevaluationresponse__student=student) & Q(studentevaluationresponse__evaluaton_event = evaluaton_event)).distinct()
                    unevaluated_courses = student.course_students.exclude(Q(id__in=evaluated_courses))

                    courses = unevaluated_courses
                    evaluation_started = True
                    context = {
                    'courses' : courses, 
                    'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'course_evaluation.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'course_evaluation.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'course_evaluation.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')






def course_evaluation_form(request,c_id):
    if request.user.is_authenticated:
        stakeholder_tag = StakeholderTag.objects.all()
        #stakeholders
        student_tag = stakeholder_tag[0]
        now = timezone.now()
        student = Student.objects.filter(user = request.user).first()
        if student:
            try:
                course = Course.objects.get(id = c_id)
            except:
                return HttpResponseNotFound("this course is not found")
            
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = student.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    factors = evaluaton_event.student_factor.all()
                    questions = Question.objects.filter(Q(factor__in = factors) & Q(stakeholder_tag = student_tag))
                    evaluation_started = True
                    context = {
                        "evaluation_event": evaluaton_event,
                       "questions" : questions,
                       'evaluation_started' : evaluation_started,
                       "course":course,
                    }
                    return render(request, 'course_evaluation_form.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'course_evaluation_form.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'course_evaluation_form.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')



def course_evaluation_save(request,c_id,e_id):
    if request.user.is_authenticated:
        student = Student.objects.filter(user = request.user).first()
        if student:
            try:
                course = Course.objects.get(id = c_id)   
            except:
                return HttpResponseNotFound("this course is not found")
            try:
                evaluation_event = EvaluationEvent.objects.get(id = e_id)
                if  evaluation_event.is_start == False:
                    return HttpResponse("evaluation event isn't started yet")
                if  evaluation_event.is_end == True:
                    return HttpResponse("evaluation event already finished")
            except:
                return HttpResponse("NO evaluation event found")
            
            if request.method == 'POST':
                # create an empty dictionary to store the question ids and answers
                answers = {}
        
                # loop through the POST data and extract the values for each question
                for key, value in request.POST.items():
                    if key.startswith('question-'):
                        # extract the question ID from the name attribute of the radio button
                        question_id = int(key.split('-')[1])
                        # store the answer value in the dictionary
                        answers[question_id] = value


                with transaction.atomic():
                    for question_id, rating in answers.items():
                        question = Question.objects.get(id = question_id)
                        student_question_response = StudentEvaluationResponse(evaluaton_event = evaluation_event,question = question,student = student,course = course,teacher = course.course_teacher,rating = str(rating))
                        student_question_response.save()
                return redirect("evaluation:course-evaluation")
            else:
                return HttpResponse("not allowed")
            
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')





def colleague_evaluation(request):
    if request.user.is_authenticated:
        now = timezone.now()
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = teacher.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    
                    teachers = Teacher.objects.filter(institution = teacher.institution).exclude(id = teacher.id)

                    evaluated_teachers = Teacher.objects.filter(
                        Q(teacherevaluationresponse__evaluator=teacher) & Q(teacherevaluationresponse__evaluaton_event = evaluaton_event)).distinct()
                    unevaluated_teachers = teachers.exclude(Q(id__in=evaluated_teachers))



                    responses = TeacherEvaluationResponse.objects.filter(evaluator=teacher, evaluaton_event=evaluaton_event)

                    # count the distinct teachers in the filtered queryset
                    evaluated_teacher_count = responses.values('teacher').distinct().count()
                    reamining_teacher = 5 - int(evaluated_teacher_count)

                    evaluation_started = True
                    context = {
                    'teacher' : teacher,
                    'teachers' : unevaluated_teachers, 
                    'evaluation_started' : evaluation_started,
                    'reamining_teacher' : reamining_teacher,
                    }
                    return render(request, 'colleague_evaluation.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'colleague_evaluation.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'colleague_evaluation.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')



def colleague_evaluation_form(request,t_id):
    if request.user.is_authenticated:
        stakeholder_tag = StakeholderTag.objects.all()
        #stakeholders
        teacher_tag = stakeholder_tag[1]
        now = timezone.now()
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            try:
                colleague = Teacher.objects.get(id = t_id)
            except:
                return HttpResponseNotFound("teacher doesn't exists")
            
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = teacher.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    factors = evaluaton_event.teacher_factor.all()
                    questions = Question.objects.filter(Q(factor__in = factors) & Q(stakeholder_tag = teacher_tag))
                    evaluation_started = True
                    context = {
                        "evaluation_event": evaluaton_event,
                       "questions" : questions,
                       'evaluation_started' : evaluation_started,
                       "colleague": colleague,
                    }
                    return render(request, 'colleague_evaluation_form.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'colleague_evaluation_form.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'colleague_evaluation_form.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')



def colleague_evaluation_save(request,t_id,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            try:
                colleague = Teacher.objects.get(id = t_id)   
            except:
                return HttpResponseNotFound("Teacher doesn't exists")
            try:
                evaluation_event = EvaluationEvent.objects.get(id = e_id)
                if  evaluation_event.is_start == False:
                    return HttpResponse("evaluation event isn't started yet")
                if  evaluation_event.is_end == True:
                    return HttpResponse("evaluation event already finished")
            except:
                return HttpResponse("NO evaluation event found")
            
            if request.method == 'POST':
                # create an empty dictionary to store the question ids and answers
                answers = {}
        
                # loop through the POST data and extract the values for each question
                for key, value in request.POST.items():
                    if key.startswith('question-'):
                        # extract the question ID from the name attribute of the radio button
                        question_id = int(key.split('-')[1])
                        # store the answer value in the dictionary
                        answers[question_id] = value


                with transaction.atomic():
                    for question_id, rating in answers.items():
                        question = Question.objects.get(id = question_id)
                        teacher_question_response = TeacherEvaluationResponse(evaluaton_event = evaluation_event, question = question, evaluator = teacher,teacher= colleague,rating = str(rating))
                        teacher_question_response.save()
                return redirect("evaluation:colleague-evaluation")
            else:
                return HttpResponse("not allowed")
            
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')


#SELF EVALUATION

def self_evaluation_form(request):
    if request.user.is_authenticated:
        stakeholder_tag = StakeholderTag.objects.all()
        #stakeholders
        self_tag = stakeholder_tag[2]
        now = timezone.now()
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = teacher.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:

                    does_exists = SelfEvaluationResponse.objects.filter(Q(evaluaton_event = evaluaton_event) & Q(teacher=teacher)).exists()
                    if does_exists:
                        evaluation_started = True
                        context = {
                        'evaluation_started' : evaluation_started,
                        "teacher" : teacher
                        }
                        return HttpResponse("self evaluation complete")
                    else:
                        factors = evaluaton_event.self_factor.all()
                        questions = Question.objects.filter(Q(factor__in = factors) & Q(stakeholder_tag = self_tag))
                        evaluation_started = True
                        context = {
                        "evaluation_event": evaluaton_event,
                        "questions" : questions,
                        'evaluation_started' : evaluation_started,
                        "teacher" : teacher,
                        }
                        return render(request, 'self_evaluation_form.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                        "teacher" : teacher,
                    }
                    return render(request, 'self_evaluation_form.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                    "teacher" : teacher,
                }
                return render(request, 'self_evaluation_form.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')



def self_evaluation_save(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            try:
                evaluation_event = EvaluationEvent.objects.get(id = e_id)
                if  evaluation_event.is_start == False:
                    return HttpResponse("evaluation event isn't started yet")
                if  evaluation_event.is_end == True:
                    return HttpResponse("evaluation event already finished")
            except:
                return HttpResponse("NO evaluation event found")
            
            if request.method == 'POST':
                # create an empty dictionary to store the question ids and answers
                answers = {}
        
                # loop through the POST data and extract the values for each question
                for key, value in request.POST.items():
                    if key.startswith('question-'):
                        # extract the question ID from the name attribute of the radio button
                        question_id = int(key.split('-')[1])
                        # store the answer value in the dictionary
                        answers[question_id] = value


                with transaction.atomic():
                    for question_id, rating in answers.items():
                        question = Question.objects.get(id = question_id)
                        teacher_question_response = SelfEvaluationResponse(evaluaton_event = evaluation_event, question = question, teacher = teacher,rating = str(rating))
                        teacher_question_response.save()
                return redirect("stakeholder:teacher-dashboard")
            else:
                return HttpResponse("not allowed")
            
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')

#PARENT EVALUATION



def course_evaluation_parent(request):
    if request.user.is_authenticated:
        now = timezone.now()
        parent = Parent.objects.filter(user = request.user).first()
        print(parent)
        if parent:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = parent.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    
                    evaluated_courses = Course.objects.filter(
                        Q(parentevaluationresponse__parent=parent) & Q(parentevaluationresponse__evaluaton_event = evaluaton_event)).distinct()
                    unevaluated_courses = parent.student.course_students.exclude(Q(id__in=evaluated_courses))

                    courses = unevaluated_courses
                    evaluation_started = True
                    context = {
                    'courses' : courses, 
                    'evaluation_started' : evaluation_started,
                    'parent' : parent,
                    }
                    return render(request, 'course_evaluation_parent.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                        'parent' : parent,
                    }
                    return render(request, 'course_evaluation_parent.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                    'parent' : parent,
                }
                return render(request, 'course_evaluation_parent.html',context)
        else:
            return HttpResponse("You are not allowed to view this-parent")
    else:
        return redirect('stakeholder:login')
    


def course_evaluation_form_parent(request,c_id):
    if request.user.is_authenticated:
        stakeholder_tag = StakeholderTag.objects.all()
        #stakeholders
        parent_tag = stakeholder_tag[3]
        now = timezone.now()
        parent = Parent.objects.filter(user = request.user).first()
        if parent:
            try:
                course = Course.objects.get(id = c_id)
            except:
                return HttpResponseNotFound("this course is not found")
            
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = parent.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    factors = evaluaton_event.parent_factor.all()
                    questions = Question.objects.filter(Q(factor__in = factors) & Q(stakeholder_tag = parent_tag))
                    evaluation_started = True
                    context = {
                        "evaluation_event": evaluaton_event,
                       "questions" : questions,
                       'evaluation_started' : evaluation_started,
                       "course":course,
                    }
                    return render(request, 'course_evaluation_form_parent.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'course_evaluation_form_parent.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'course_evaluation_form_parent.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')


def course_evaluation_parent_save(request,c_id,e_id):
    if request.user.is_authenticated:
        parent = Parent.objects.filter(user = request.user).first()
        if parent:
            try:
                course = Course.objects.get(id = c_id)   
            except:
                return HttpResponseNotFound("this course is not found")
            try:
                evaluation_event = EvaluationEvent.objects.get(id = e_id)
                if  evaluation_event.is_start == False:
                    return HttpResponse("evaluation event isn't started yet")
                if  evaluation_event.is_end == True:
                    return HttpResponse("evaluation event already finished")
            except:
                return HttpResponse("NO evaluation event found")
            
            if request.method == 'POST':
                # create an empty dictionary to store the question ids and answers
                answers = {}
        
                # loop through the POST data and extract the values for each question
                for key, value in request.POST.items():
                    if key.startswith('question-'):
                        # extract the question ID from the name attribute of the radio button
                        question_id = int(key.split('-')[1])
                        # store the answer value in the dictionary
                        answers[question_id] = value


                with transaction.atomic():
                    for question_id, rating in answers.items():
                        question = Question.objects.get(id = question_id)
                        parent_question_response = ParentEvaluationResponse(evaluaton_event = evaluation_event,question = question,parent = parent,course = course,teacher = course.course_teacher,rating = str(rating))
                        parent_question_response.save()
                return redirect("evaluation:course-evaluation-parent")
            else:
                return HttpResponse("not allowed")
            
        else:
            return HttpResponse("You are not allowed to view this->parent")
    else:
        return redirect('stakeholder:login')




def teacher_evaluation_administrations(request):
    if request.user.is_authenticated:
        now = timezone.now()
        administrator = Administrator.objects.filter(user = request.user).first()
        if administrator:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = administrator.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    
                    teachers = Teacher.objects.filter(institution = administrator.institution)

                    evaluated_teachers = Teacher.objects.filter(
                        Q(administrationevaluationresponse__administrator=administrator) & Q(administrationevaluationresponse__evaluaton_event = evaluaton_event)).distinct()
                    unevaluated_teachers = teachers.exclude(Q(id__in=evaluated_teachers))

                    responses = AdministrationEvaluationResponse.objects.filter(administrator=administrator, evaluaton_event=evaluaton_event)

                    total_teacher = Teacher.objects.filter(institution= administrator.institution).count()
                    # count the distinct teachers in the filtered queryset
                    evaluated_teacher_count = responses.values('teacher').distinct().count()
                    reamining_teacher = total_teacher - int(evaluated_teacher_count)

                    evaluation_started = True
                    context = {
                    'administrator' : administrator,
                    'teachers' : unevaluated_teachers, 
                    'evaluation_started' : evaluation_started,
                    'reamining_teacher' : reamining_teacher,
                    }
                    return render(request, 'teacher_evaluation_administration.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'administrator' : administrator,
                        'evaluation_started' : evaluation_started,
                    }
                    return render(request, 'teacher_evaluation_administration.html',context)
            else:
                evaluation_started = False
                context = {
                    'administrator' : administrator,
                    'evaluation_started' : evaluation_started,
                }
                return render(request, 'teacher_evaluation_administration.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')


def teacher_evaluation_administration_form(request,t_id):
    if request.user.is_authenticated:
        stakeholder_tag = StakeholderTag.objects.all()
        #stakeholders
        administrator_tag = stakeholder_tag[4]
        now = timezone.now()
        administrator = Administrator.objects.filter(user = request.user).first()
        if administrator:
            try:
                teacher = Teacher.objects.get(id = t_id)
            except:
                return HttpResponseNotFound("teacher doesn't exists")
            
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = administrator.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                start_time = timezone.make_aware(datetime.combine(evaluaton_event.start_date, time.min))
                end_time = timezone.make_aware(datetime.combine(evaluaton_event.end_date, time.max))
                if start_time <= now <= end_time:
                    factors = evaluaton_event.administrator_factor.all()
                    questions = Question.objects.filter(Q(factor__in = factors) & Q(stakeholder_tag = administrator_tag))
                    evaluation_started = True
                    context = {
                        "evaluation_event": evaluaton_event,
                       "questions" : questions,
                       'evaluation_started' : evaluation_started,
                       "teacher": teacher,
                       'administrator' : administrator,
                    }
                    return render(request, 'teacher_evaluation_administration_form.html',context)
                else:
                    evaluation_started = False
                    context = {
                        'evaluation_started' : evaluation_started,
                        'administrator' : administrator,
                    }
                    return render(request, 'teacher_evaluation_administration_form.html',context)
            else:
                evaluation_started = False
                context = {
                    'evaluation_started' : evaluation_started,
                    'administrator' : administrator,
                }
                return render(request, 'teacher_evaluation_administration_form.html',context)
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')
    



def teacher_evaluation_administration_save(request,t_id,e_id):
    if request.user.is_authenticated:
        administrator = Administrator.objects.filter(user = request.user).first()
        if administrator:
            try:
                teacher = Teacher.objects.get(id = t_id)   
            except:
                return HttpResponseNotFound("Teacher doesn't exists")
            try:
                evaluation_event = EvaluationEvent.objects.get(id = e_id)
                if  evaluation_event.is_start == False:
                    return HttpResponse("evaluation event isn't started yet")
                if  evaluation_event.is_end == True:
                    return HttpResponse("evaluation event already finished")
            except:
                return HttpResponse("NO evaluation event found")
            
            if request.method == 'POST':
                # create an empty dictionary to store the question ids and answers
                answers = {}
        
                # loop through the POST data and extract the values for each question
                for key, value in request.POST.items():
                    if key.startswith('question-'):
                        # extract the question ID from the name attribute of the radio button
                        question_id = int(key.split('-')[1])
                        # store the answer value in the dictionary
                        answers[question_id] = value


                with transaction.atomic():
                    for question_id, rating in answers.items():
                        question = Question.objects.get(id = question_id)
                        teacher_question_response = AdministrationEvaluationResponse(evaluaton_event = evaluation_event, question = question, administrator = administrator,teacher= teacher,rating = str(rating))
                        teacher_question_response.save()
                return redirect("evaluation:teacher-evaluation-administrator")
            else:
                return HttpResponse("not allowed")
            
        else:
            return HttpResponse("You are not allowed to view this")
    else:
        return redirect('stakeholder:login')





def current_evaluation_report_view(request):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(Q(institution = teacher.institution) & Q(is_start = True) & Q(is_end = False)).first()
            if evaluaton_event:
                if request.method == 'GET':
                    context = {
                        'evaluation':evaluaton_event,
                        'teacher':teacher,
                    }
                    return render(request, 'current_evaluation_report.html',context)
            else:
                return HttpResponse("there is no on going evaluation right now")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')


def student_evaluation_report(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(id = e_id).first()
            if evaluaton_event:

                responses = StudentEvaluationResponse.objects.filter(
                    evaluaton_event=evaluaton_event, teacher=teacher
                ).select_related('question').order_by('question')

                response_dict = {str(q.id): [r.rating for r in group] for q, group in itertools.groupby(responses, lambda r: r.question)}

                question_ids = list(response_dict.keys())
                questions = Question.objects.filter(id__in=question_ids)

                data = [go.Bar(x=list(response_dict.keys()), y=[sum(map(int, v))/len(v) for v in response_dict.values()])]

                layout = go.Layout(title='Teacher Evaluation Results', xaxis=dict(title='Question ID'), yaxis=dict(title='Average Rating'))

                chart_html = plot({'data': data, 'layout': layout}, output_type='div')


                #for each questions
                plot_divs = {}
                for question, ratings in response_dict.items():
                    quesiton_obj = Question.objects.filter(id = question).first()
                    y_value = []
                    sum_ = 0
                    avg = 0
                    for i in range(len(ratings)):
                        sum_ = (sum_ + int(ratings[i]))
                        avg = sum_/(i+1)
                        y_value.append(avg)

                    x_axis = [f'{i+1}' for i in range(len(ratings))]
                    y_axis = y_value

                    trace = go.Scatter(
                        x=x_axis,
                        y=y_axis,
                        mode='lines+markers'
                    )

                    layout = go.Layout(
                        title=quesiton_obj.question,
                        xaxis=dict(
                            title='Responses'
                        ),
                        yaxis=dict(
                            title='Average Ratings',
                            range=[0, 5] # set y-axis limit
                        )
                    )

                    fig = go.Figure(data=[trace], layout=layout)

                    plot_divs[question] = fig.to_html(full_html=False)

                
                context = {
                    'chart_html' : chart_html,
                    'questions' : questions,
                    'plot_divs' : plot_divs,
                    'teacher' : teacher,
                }

                return render(request,'student_evaluation_report.html',context)
            else:
                return HttpResponse("no evaluation exists under this id")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')
    

def colleague_evaluation_report(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(id = e_id).first()
            if evaluaton_event:

                responses = TeacherEvaluationResponse.objects.filter(
                    evaluaton_event=evaluaton_event, teacher=teacher
                ).select_related('question').order_by('question')

                response_dict = {str(q.id): [r.rating for r in group] for q, group in itertools.groupby(responses, lambda r: r.question)}

                question_ids = list(response_dict.keys())
                questions = Question.objects.filter(id__in=question_ids)

                data = [go.Bar(x=list(response_dict.keys()), y=[sum(map(int, v))/len(v) for v in response_dict.values()])]

                layout = go.Layout(title='Teacher Evaluation Results', xaxis=dict(title='Question ID'), yaxis=dict(title='Average Rating'))

                chart_html = plot({'data': data, 'layout': layout}, output_type='div')


                #for each questions
                plot_divs = {}
                for question, ratings in response_dict.items():
                    quesiton_obj = Question.objects.filter(id = question).first()
                    y_value = []
                    sum_ = 0
                    avg = 0
                    for i in range(len(ratings)):
                        sum_ = (sum_ + int(ratings[i]))
                        avg = sum_/(i+1)
                        y_value.append(avg)

                    x_axis = [f'{i+1}' for i in range(len(ratings))]
                    y_axis = y_value

                    trace = go.Scatter(
                        x=x_axis,
                        y=y_axis,
                        mode='lines+markers'
                    )

                    layout = go.Layout(
                        title=quesiton_obj.question,
                        xaxis=dict(
                            title='Responses'
                        ),
                        yaxis=dict(
                            title='Average Ratings',
                            range=[0, 5] # set y-axis limit
                        )
                    )

                    fig = go.Figure(data=[trace], layout=layout)

                    plot_divs[question] = fig.to_html(full_html=False)

                
                context = {
                    'chart_html' : chart_html,
                    'questions' : questions,
                    'plot_divs' : plot_divs,
                    'teacher' : teacher,
                }

                return render(request,'colleague_evaluation_report.html',context)
            else:
                return HttpResponse("no evaluation exists under this id")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')
    



def parent_evaluation_report(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(id = e_id).first()
            if evaluaton_event:

                responses = ParentEvaluationResponse.objects.filter(
                    evaluaton_event=evaluaton_event, teacher=teacher
                ).select_related('question').order_by('question')

                response_dict = {str(q.id): [r.rating for r in group] for q, group in itertools.groupby(responses, lambda r: r.question)}

                question_ids = list(response_dict.keys())
                questions = Question.objects.filter(id__in=question_ids)

                data = [go.Bar(x=list(response_dict.keys()), y=[sum(map(int, v))/len(v) for v in response_dict.values()])]

                layout = go.Layout(title='Teacher Evaluation Results', xaxis=dict(title='Question ID'), yaxis=dict(title='Average Rating'))

                chart_html = plot({'data': data, 'layout': layout}, output_type='div')


                #for each questions
                plot_divs = {}
                for question, ratings in response_dict.items():
                    quesiton_obj = Question.objects.filter(id = question).first()
                    y_value = []
                    sum_ = 0
                    avg = 0
                    for i in range(len(ratings)):
                        sum_ = (sum_ + int(ratings[i]))
                        avg = sum_/(i+1)
                        y_value.append(avg)

                    x_axis = [f'{i+1}' for i in range(len(ratings))]
                    y_axis = y_value

                    trace = go.Scatter(
                        x=x_axis,
                        y=y_axis,
                        mode='lines+markers'
                    )

                    layout = go.Layout(
                        title=quesiton_obj.question,
                        xaxis=dict(
                            title='Responses'
                        ),
                        yaxis=dict(
                            title='Average Ratings',
                            range=[0, 5] # set y-axis limit
                        )
                    )

                    fig = go.Figure(data=[trace], layout=layout)

                    plot_divs[question] = fig.to_html(full_html=False)

                
                context = {
                    'chart_html' : chart_html,
                    'questions' : questions,
                    'plot_divs' : plot_divs,
                    'teacher' : teacher,
                }

                return render(request,'parent_evaluation_report.html',context)
            else:
                return HttpResponse("no evaluation exists under this id")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')
    

def administrator_evaluation_report(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(id = e_id).first()
            if evaluaton_event:

                responses = AdministrationEvaluationResponse.objects.filter(
                    evaluaton_event=evaluaton_event, teacher=teacher
                ).select_related('question').order_by('question')

                response_dict = {str(q.id): [r.rating for r in group] for q, group in itertools.groupby(responses, lambda r: r.question)}

                question_ids = list(response_dict.keys())
                questions = Question.objects.filter(id__in=question_ids)

                data = [go.Bar(x=list(response_dict.keys()), y=[sum(map(int, v))/len(v) for v in response_dict.values()])]

                layout = go.Layout(title='Teacher Evaluation Results', xaxis=dict(title='Question ID'), yaxis=dict(title='Average Rating'))

                chart_html = plot({'data': data, 'layout': layout}, output_type='div')


                #for each questions
                plot_divs = {}
                for question, ratings in response_dict.items():
                    quesiton_obj = Question.objects.filter(id = question).first()
                    y_value = []
                    sum_ = 0
                    avg = 0
                    for i in range(len(ratings)):
                        sum_ = (sum_ + int(ratings[i]))
                        avg = sum_/(i+1)
                        y_value.append(avg)

                    x_axis = [f'{i+1}' for i in range(len(ratings))]
                    y_axis = y_value

                    trace = go.Scatter(
                        x=x_axis,
                        y=y_axis,
                        mode='lines+markers'
                    )

                    layout = go.Layout(
                        title=quesiton_obj.question,
                        xaxis=dict(
                            title='Responses'
                        ),
                        yaxis=dict(
                            title='Average Ratings',
                            range=[0, 5] # set y-axis limit
                        )
                    )

                    fig = go.Figure(data=[trace], layout=layout)

                    plot_divs[question] = fig.to_html(full_html=False)

                
                context = {
                    'chart_html' : chart_html,
                    'questions' : questions,
                    'plot_divs' : plot_divs,
                    'teacher' : teacher,
                }

                return render(request,'administrator_evaluation_report.html',context)
            else:
                return HttpResponse("no evaluation exists under this id")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')
    


def self_evaluation_report(request,e_id):
    if request.user.is_authenticated:
        teacher = Teacher.objects.filter(user = request.user).first()
        if teacher:
            evaluaton_event = EvaluationEvent.objects.filter(id = e_id).first()
            if evaluaton_event:

                responses = SelfEvaluationResponse.objects.filter(
                    evaluaton_event=evaluaton_event, teacher=teacher
                ).select_related('question').order_by('question')

                response_dict = {str(q.id): [r.rating for r in group] for q, group in itertools.groupby(responses, lambda r: r.question)}

                question_ids = list(response_dict.keys())
                questions = Question.objects.filter(id__in=question_ids)

                data = [go.Bar(x=list(response_dict.keys()), y=[sum(map(int, v))/len(v) for v in response_dict.values()])]

                layout = go.Layout(title='Teacher Evaluation Results', xaxis=dict(title='Question ID'), yaxis=dict(title='Average Rating'))

                chart_html = plot({'data': data, 'layout': layout}, output_type='div')


                
                
                context = {
                    'chart_html' : chart_html,
                    'questions' : questions,
                    'teacher' : teacher,
                }

                return render(request,'administrator_evaluation_report.html',context)
            else:
                return HttpResponse("no evaluation exists under this id")
        else:
            return HttpResponse("you are not allowed to view this")
    else:
        return redirect('stakeholder:login')