from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from stakeholder.models import Institution, Student, Parent, Department, Teacher, Course, Administrator
from evaluation.models import StakeholderTag, InstitutionTag
import json


class TestViews(TestCase):

    def setUp(self):
        StakeholderTag.objects.create(name="Student")
        StakeholderTag.objects.create(name="Teacher")
        StakeholderTag.objects.create(name="Self")
        StakeholderTag.objects.create(name="Parent")
        StakeholderTag.objects.create(name="Administrator")

        InstitutionTag.objects.create(name="Primary")
        InstitutionTag.objects.create(name="Secondary")
        InstitutionTag.objects.create(name="Tertiary")

        institution = Institution(
            institution_name="Hello institution",
            institution_code="12345",
            established_year="2022",
            institution_type="Tertiary",
            institution_head="Mr unknown",
            location="Dhaka",
        )

        institution._full_name = "Shahparan Rifat"
        institution._email = "rifat@gmail.com"
        institution._username = "rifat1"
        institution._password = "1234"

        institution.save()

        self.institution = institution

    def test_register_view_GET(self):
        client = Client()
        response = client.get(reverse("stakeholder:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_POST(self):
        client = Client()
        response = client.post('/register/', {
            'institution_name': 'Unknown institution',
            'institution_code': '12345',
            'established_year': '2022',
            'institution_type': '1',
            'institution_head': 'Mr Unknown',
            'location': 'Dhaka',
            'fullname': 'Shahparan Rifat',
            'email': 'rifat@gmail.com',
            'username': 'rifat',
            'password': '1234',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Institution.objects.all()[1].institution_name, "Unknown institution")

    def test_login_view_GET(self):
        client = Client()
        response = client.get(reverse("stakeholder:login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_POST(self):
        client = Client()
        response = client.post(reverse("stakeholder:login"), {
            'username': 'rifat1',
            'password': '1234',
        })
        self.assertRedirects(response, expected_url=reverse('stakeholder:admin-dashboard'), status_code=302)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    
    def test_add_student_view_POST(self):
        client = Client()
        client.login(username = 'rifat1', password = '1234')
        department = Department(name= "computer science",dept_head="Mr Unknown",institution=self.institution)
        department.save()
        response = client.post(reverse("stakeholder:add-student"), {
                'first_name': 'Shahparan',
                'last_name' : 'Rifat',
                'student_id' : '011191150',
                'father_name' : 'Abdur Rahim',
                'mother_name' : 'Momtaz Begum',
                'gender' : '1',
                'dob' : '1998-07-12',
                'phone' : '01879944474',
                'department' : '1',
                'student_username' : 'rifat_s',
                'email' : 'rifat@gmail.com',
                'student_password' : '1234',
                'parent_username' : 'rifat_p',
                'parent_phone' : '01731591872',
                'parent_password' : '1234',
                'address' : 'Madhabdi',
                'city' : 'Narsingdi',
                'state' : 'Dhaka',
                'zipcode' : '1204',
        })
        self.assertRedirects(response, expected_url=reverse('stakeholder:student-list'), status_code=302)
        self.assertEquals(Student.objects.first().first_name, "Shahparan")
