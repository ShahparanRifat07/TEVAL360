from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


GENDER_CHOICE = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Others"),
)

INSTITUTION_TYPE = (
    ("1","Primary"),
    ("2","Secondary"),
    ("3","Tertiary"),
    ("4","Other"),
)


class Institution(models.Model):
    institution_name = models.CharField(max_length=128)
    institution_code = models.CharField(max_length=11)
    established_year = models.CharField(max_length=4)
    institution_type = models.CharField(max_length = 1, choices = INSTITUTION_TYPE)
    institution_head = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    institution_admin = models.OneToOneField(User, on_delete=models.CASCADE)
    apply_date = models.DateField(default=timezone.now)
    approved = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self._full_name

    @property
    def email(self):
        return self._email

    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password


    def __str__(self):
        return self.institution_name

class Department(models.Model):
    name = models.CharField(max_length=128)
    dept_head = models.CharField(max_length=64)
    description = models.TextField(null=True,blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name




class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    student_id = models.CharField(max_length=11)
    father_name = models.CharField(max_length=64)
    mother_name = models.CharField(max_length=64)
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICE)
    dob = models.DateField(blank=True,null=True)
    phone_number = models.CharField(max_length=16)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64,blank=True,null=True)
    state = models.CharField(max_length=64,blank=True,null=True)
    zipcode = models.CharField(max_length=64,blank=True,null=True)
    image = models.ImageField(upload_to='Profile_Picture', default='default.jpg')

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=64)


    @property
    def student_username(self):
        return self._student_username
    
    @property
    def student_password(self):
        return self._student_password


    @property
    def parent_username(self):
        return self._parent_username

    @property
    def parent_phone_number(self):
        return self._parent_phone_number

    @property
    def parent_password(self):
        return self._parent_password

    def __str__(self):
        return self.first_name+" "+self.last_name


class Parent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Profile_Picture', default='default.jpg')

    def __str__(self):
        return self.user.username




class Teacher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    teacher_id = models.CharField(max_length=32)
    designation = models.CharField(max_length=64)
    joining_date = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICE)
    dob = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=16)
    image = models.ImageField(upload_to='Profile_Picture', default='default.jpg')
    email = models.CharField(max_length=64)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64,blank=True,null=True)
    state = models.CharField(max_length=64,blank=True,null=True)
    zipcode = models.CharField(max_length=64,blank=True,null=True)

    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)


    @property
    def teacher_username(self):
        return self._teacher_username
    
    @property
    def teacher_password(self):
        return self._teacher_password

    def __str__(self):
        return self.first_name+" "+self.last_name
    

class Administrator(models.Model):
    first_name = models.CharField(max_length=64,null=True,blank=True)
    last_name = models.CharField(max_length=64,null=True,blank=True)
    administrative_id = models.CharField(max_length=64,null=True,blank=True)
    role = models.CharField(max_length=128,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='Profile_Picture', default='default.jpg')

    @property
    def administrator_username(self):
        return self._administrator_username
    
    @property
    def administrator_password(self):
        return self._administrator_password
    
    @property
    def administrator_email(self):
        return self._administrator_email
    
    @property
    def add_teacher(self):
        return self._add_teacher
    
    @property
    def add_student(self):
        return self._add_student
    
    @property
    def add_course(self):
        return self._add_course
    
    @property
    def edit_teacher(self):
        return self._edit_teacher
    
    @property
    def edit_student(self):
        return self._edit_student
    
    @property
    def edit_course(self):
        return self._edit_course
    
    def __str__(self):
        return self.first_name+" "+self.last_name



class Course(models.Model):
    course_id = models.CharField(max_length=16)
    course_name = models.CharField(max_length=128)
    section = models.CharField(max_length=2)
    course_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True)
    course_students = models.ManyToManyField(Student, related_name='course_students')
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

        