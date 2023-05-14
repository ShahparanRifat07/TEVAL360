from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Institution,Student,Parent,Department,Teacher,Course,Administrator
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from .resources import StudentResource
from tablib import Dataset
from django.urls import reverse
import os
from django.db import transaction
from core.settings import BASE_DIR
from .utility import valided_add_student_form
from django.core import serializers
from django.db.models import Q
# Create your views here.


def register(request):
    if request.method == "POST":
        institution_name = request.POST.get("institution_name")
        institution_code = request.POST.get("institution_code")
        established_year = request.POST.get("established_year")
        institution_type = request.POST.get("institution_type")
        institution_head = request.POST.get("institution_head")
        location = request.POST.get("location")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        institution = Institution(institution_name=institution_name, institution_code=institution_code,
                                  established_year=established_year, institution_type=institution_type, institution_head=institution_head,
                                  location=location)

        institution._full_name = fullname
        institution._email = email
        institution._username = username
        institution._password = password

        institution.save()

        return redirect("stakeholder:login")
    elif request.method == "GET":
        return render(request, "register.html")

def admin_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        institution = Institution.objects.filter(institution_admin=user)
        if institution:
            student_number = Student.objects.all().count()
            if user.last_login is None:
                first_time_login = True
            else:
                first_time_login = False
            context={
                'student_number' : student_number,
                'admin' : institution[0].institution_admin,
                'first_time': first_time_login
            }
            return render(request,'admin_dashboard.html',context)
        else:
            return HttpResponse("you are not an admin")
    else:
        return redirect('stakeholder:login')


def student_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        student = Student.objects.get(user= user)
        if student is not None:
            context = {
                'student' : student,
            }
            return render(request,'student_dashboard.html',context)
        else:
            return HttpResponse("You are not a student")
    else:
        return redirect('stakeholder:login')
    

def parent_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        parent = Parent.objects.get(user= user)
        if parent is not None:
            context = {
                'parent' : parent,
            }
            return render(request,'parent_dashboard.html',context)
        else:
            return HttpResponse("You are not a Parent")
    else:
        return redirect('stakeholder:login')
    
def teacher_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        teacher = Teacher.objects.get(user= user)
        if teacher is not None:
            context = {
                'teacher' : teacher,
            }
            return render(request,'teacher_dashboard.html',context)
        else:
            return HttpResponse("You are not a Teacher")
    else:
        return redirect('stakeholder:login')
    

def administrator_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        administrator = Administrator.objects.get(user= user)
        if administrator is not None:
            context = {
                'administrator' : administrator,
            }
            return render(request,'administrator_dashboard.html',context)
        else:
            return HttpResponse("You are not a Administrator")
    else:
        return redirect('stakeholder:login')

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        institution_admin = Institution.objects.filter(institution_admin=user)
        if institution_admin:
            return redirect("stakeholder:admin-dashboard")
        else:
            student = Student.objects.filter(user= user).first()
            print(student)
            if student is not None:
                return redirect("stakeholder:student-dashboard")
            else:
                parent = Parent.objects.filter(user= user).first()
                if parent is not None:
                    return redirect("stakeholder:parent-dashboard")
                else:
                    teacher = Teacher.objects.filter(user= user).first()
                    if teacher is not None:
                        return redirect("stakeholder:teacher-dashboard")
                    else:
                        administrator = Administrator.objects.filter(user= user).first()
                        if administrator is not None:
                            return redirect("stakeholder:administrator-dashboard")
                        else:
                            return redirect('stakeholder:login')
    else:
        return redirect('stakeholder:login')
        

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(username= username,password = password)

            if user is not None:
                login(request,user)
                return dashboard(request)
            else:
                print("no user found---method=>user_login")
                return redirect("stakeholder:login")
        except:
            print("user does not exits==user_login")
            return redirect("stakeholder:login")
    elif request.method == "GET":
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('stakeholder:login')



#Student
def add_student(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            institution_admin = institution[0].institution_admin
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                student_id = request.POST.get('student_id')
                father_name = request.POST.get('father_name')
                mother_name = request.POST.get('mother_name')
                gender = request.POST.get('gender')
                dob = request.POST.get('dob')
                phone = request.POST.get('phone')
                department = request.POST.get('department')
                student_username = request.POST.get('student_username')
                email = request.POST.get('email')
                student_password = request.POST.get('student_password')
                parent_username = request.POST.get('parent_username')
                parent_phone = request.POST.get('parent_phone')
                parent_password = request.POST.get('parent_password')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                zipcode = request.POST.get('zipcode')


                valided_add_student_form(first_name,last_name,student_id,father_name,mother_name,gender,dob,phone,
                                         department,student_username,student_password,email,parent_username,
                                         parent_password,parent_phone)


                dept = Department.objects.get(id=department)
                student = Student(first_name = first_name,last_name = last_name,student_id = student_id,father_name=father_name,
                                    mother_name = mother_name, gender = gender,dob=dob,phone_number = phone,email = email,
                                    address = address,city=city,state=state,zipcode=zipcode,institution= institution[0],department = dept)
                

                student._student_username = student_username
                student._student_password = student_password
                student._parent_username = parent_username
                student._parent_phone_number = parent_phone
                student._parent_password = parent_password

                student.save()

                return redirect('stakeholder:student-list')
            if request.method == 'GET':
                departments = Department.objects.filter(institution = institution[0])
                context = {
                    'departments' : departments,
                    'admin' : institution[0].institution_admin,
                }
                return render(request,'add_student.html',context)
        else:
            return HttpResponse("You are not allowed")
    else:
        return redirect('stakeholder:login')


def add_student_excel(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            institution_admin = institution[0].institution_admin
            if request.method == 'POST':
                student_resource = StudentResource()
                dataset = Dataset()
                new_student = request.FILES['file']

                if not new_student.name.endswith('xlsx'):
                    return HttpResponse("Wrong Format")
                
                imported_data = dataset.load(new_student.read(),format='xlsx')
                with transaction.atomic():
                    for data in imported_data:
                            depart = Department.objects.get(id=data[13],institution=institution[0])
                            student = Student(first_name = data[1],last_name = data[2],student_id =data[3],father_name=data[4],mother_name=data[5],
                                            gender=data[6],dob=data[7],phone_number=str(data[8]),address=data[9],city=data[10],state=data[11],zipcode=str(data[12]),
                                            department = depart,email=data[14],institution = institution[0])

                            student._student_username = data[15]
                            student._student_password = str(data[16])
                            student._parent_username = data[17]
                            student._parent_phone_number = str(data[18])
                            student._parent_password = str(data[19])

                            student.save()
                
                return render(request,'excel_add_students.html')

            if request.method == 'GET':
                context = {
                    'admin' : institution[0].institution_admin,
                }
                return render(request,'excel_add_students.html',context)
        else:
            return HttpResponse("You are not allowed")
    else:
        return redirect('stakeholder:login')
    


def download_student_excel(request):
    file_path = BASE_DIR / 'static/file/student_upload_template.xlsx'
    if os.path.exists(file_path):
        with open(file_path, "rb") as excel:
            data = excel.read()

        response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=add_student.xlsx'
        return response
    

def view_student_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            students = Student.objects.filter(institution=institution[0])
            context={
                "students" : students,
                'admin' : institution[0].institution_admin,
            }
            return render(request,'student_list.html',context)
        else:
            return HttpResponse("You are not allowed")
    else:
        return redirect('stakeholder:login')






#Teacher
def add_teacher(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            institution_admin = institution[0].institution_admin
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                teacher_id = request.POST.get('teacher_id')
                designation = request.POST.get('designation')
                joining_date = request.POST.get('joining_date')
                gender = request.POST.get('gender')
                dob = request.POST.get('dob')
                phone = request.POST.get('phone')
                department = request.POST.get('department')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                zipcode = request.POST.get('zipcode')


                dept = Department.objects.get(id=department)
                teacher = Teacher(first_name=first_name,last_name=last_name,teacher_id=teacher_id,designation=designation,joining_date=joining_date,
                            gender=gender,dob=dob,phone=phone,email=email,address=address,city=city,state=state,zipcode=zipcode,department=dept,
                            institution=institution[0])

                teacher._teacher_username = username
                teacher._teacher_password = password

                teacher.save()

                return redirect('stakeholder:teacher-list')
            if request.method == 'GET':
                departments = Department.objects.filter(institution = institution[0])
                context = {
                    'departments' : departments,
                    'admin' : institution[0].institution_admin,
                }
                return render(request,'add_teacher.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')



def view_teacher_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            teachers = Teacher.objects.filter(institution=institution[0])
            context={
                "teachers" : teachers,
                'admin' : institution[0].institution_admin,
            }
            return render(request,'teacher_list.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')





#Administrator

def add_administrator(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                id = request.POST.get('id')
                phone = request.POST.get('phone')
                role =request.POST.get('role')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                add_teacher = request.POST.get('add-teacher')
                add_student = request.POST.get('add-student')
                add_course = request.POST.get('add-course')
                edit_teacher = request.POST.get('edit-teacher')
                edit_student = request.POST.get('edit-student')
                edit_course = request.POST.get('edit-course')


                administrator = Administrator(first_name=first_name,last_name=last_name,administrative_id = id,role=role,phone=phone,institution=institution)
                administrator._administrator_username = username
                administrator._administrator_password = password
                administrator._administrator_email = email
                administrator._add_teacher = add_teacher
                administrator._add_student = add_student
                administrator._add_course = add_course
                administrator._edit_teacher = edit_teacher
                administrator._edit_student = edit_student
                administrator._edit_course = edit_course

                administrator.save()
                
                return redirect('stakeholder:administrator-list')
            if request.method == 'GET':
                context = {
                    'admin' : institution.institution_admin,
                }
                return render(request,'add_administrator.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')


def view_administrator_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            administrators = Administrator.objects.filter(institution=institution[0])
            context={
                "administrators" : administrators,
                'admin' : institution[0].institution_admin,
            }
            return render(request,'administrator_list.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')



#Department
def add_department(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            institution_admin = institution[0].institution_admin
            if request.method == 'POST':
                name = request.POST.get('name')
                dept_head = request.POST.get('head')
                description =request.POST.get('description')

                department = Department(name=name,dept_head=dept_head,description=description,institution=institution[0])
                department.save()

                return redirect('stakeholder:department-list')
            if request.method == 'GET':
                context = {
                    'admin' : institution[0].institution_admin,
                }
                return render(request,'add_department.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')




def view_department_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            departments = Department.objects.filter(institution=institution[0])
            context={
                "departments" : departments,
                'admin' : institution[0].institution_admin,
            }
            return render(request,'department_list.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    





#Course
def add_course(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user)
        if institution:
            if request.method == 'POST':
                id = request.POST.get('course_id')
                name = request.POST.get('course_name')
                section =request.POST.get('course_section')

                course = Course(course_id = id, course_name = name, section = section,institution = institution[0])
                course.save()

                return redirect('stakeholder:course-list')
            if request.method == 'GET':
                context = {
                    'admin' : institution[0].institution_admin,
                }
                return render(request,'add_course.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')


def course_list(request):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            courses = Course.objects.filter(institution=institution)
            context={
                "courses" : courses,
                'admin' : institution.institution_admin,
            }
            return render(request,'course_list.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')

def assign_course_to_student(request,cid):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
                enrolled_students = course.course_students.all()
                unenrolled_students = Student.objects.filter(institution=institution).exclude(pk__in=[item.pk for item in enrolled_students])
            except:
                return HttpResponseNotFound("Not found")
            if request.method == 'GET':
                context = {
                    'course' : course,
                    'students' : unenrolled_students,
                    'admin' : institution.institution_admin,
                }
                return render(request,'assign_student.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')

def assign_student(request,cid,sid):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
                student = Student.objects.get(id = sid)
            except:
                return HttpResponseNotFound("Not found")
            
            if student.course_students.filter(pk=course.pk).exists():
                return  HttpResponse("can not add course...already assigned")
            else:
                course.course_students.add(student)
                return redirect('stakeholder:course-list')
            
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    

def assign_course_to_teacher(request,cid):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
            except:
                return HttpResponseNotFound("Not found")
            if course.course_teacher is None:
                teachers = Teacher.objects.filter(institution = institution)
            else:
                teachers = Teacher.objects.filter(institution = institution).exclude(pk = course.course_teacher.pk)

            if request.method == 'GET':
                context = {
                    'course' : course,
                    'teachers' : teachers,
                    'admin' : institution.institution_admin,
                }
                return render(request,'assign_teacher.html',context)
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    


def assign_teacher(request,cid,tid):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
                teacher = Teacher.objects.get(id = tid)
            except:
                return HttpResponseNotFound("Not found")
            if course.course_teacher is not None:
                return  HttpResponse("can not assign teacher...already assigned")
            else:
                course.course_teacher = teacher
                course.save()
                return redirect('stakeholder:course-list')
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')



def student_list_json(request,cid,name):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
            except:
                return  HttpResponseNotFound("Not found")
            if course.institution == institution:
                enrolled_students = course.course_students.all()
                unenrolled_students = Student.objects.filter(institution=institution).exclude(pk__in=[item.pk for item in enrolled_students])
                qs = unenrolled_students.filter(Q(first_name__contains=name) | Q(last_name__contains = name))
                qs_json = serializers.serialize('json', qs)
                return HttpResponse(qs_json, content_type='application/json')
            else:
                raise PermissionDenied("You are not allowed")
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    
def student_list_all_json(request,cid):
    if request.user.is_authenticated:
        institution = Institution.objects.filter(institution_admin=request.user).first()
        if institution:
            try:
                course = Course.objects.get(id = cid)
            except:
                return  HttpResponseNotFound("Not found")
            if course.institution == institution:
                enrolled_students = course.course_students.all()
                unenrolled_students = Student.objects.filter(institution=institution).exclude(pk__in=[item.pk for item in enrolled_students])
                qs_json = serializers.serialize('json', unenrolled_students)
                return HttpResponse(qs_json, content_type='application/json')
            else:
                    raise PermissionDenied("You are not allowed")
        else:
            raise PermissionDenied("You are not allowed")
    else:
        return redirect('stakeholder:login')
    