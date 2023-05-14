from django.test import SimpleTestCase
from django.urls import reverse,resolve
from stakeholder.views import (register,user_login,add_student,user_logout,add_teacher,add_student_excel,
                    add_course,assign_course_to_student,assign_course_to_teacher)


class TestUrls(SimpleTestCase):

    def test_register_url_is_okay(self):
        url = reverse('stakeholder:register')
        self.assertEquals(resolve(url).func,register)

    def test_login_url_is_okay(self):
        url = reverse('stakeholder:login')
        self.assertEquals(resolve(url).func,user_login)
    
    def test_logout_url_is_okay(self):
        url = reverse('stakeholder:logout')
        self.assertEquals(resolve(url).func,user_logout)

    def test_add_student_url_is_okay(self):
        url = reverse('stakeholder:add-student')
        self.assertEquals(resolve(url).func,add_student)
    
    def test_add_student_excel_url_is_okay(self):
        url = reverse('stakeholder:add-student-excel')
        self.assertEquals(resolve(url).func,add_student_excel)
    
    def test_add_teacher_url_is_okay(self):
        url = reverse('stakeholder:add-teacher')
        self.assertEquals(resolve(url).func,add_teacher)

    def test_add_course_url_is_okay(self):
        url = reverse('stakeholder:add-course')
        self.assertEquals(resolve(url).func,add_course)
    
    def test_assign_course_student_url_is_okay(self):
        url = reverse('stakeholder:assign-course-student',args=['1'])
        self.assertEquals(resolve(url).func,assign_course_to_student)
    
    def test_assign_course_teacher_url_is_okay(self):
        url = reverse('stakeholder:assign-course-teacher',args=['1'])
        self.assertEquals(resolve(url).func,assign_course_to_teacher)