from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from stakeholders.models import Institution, Student, Parent,Teacher
from evaluation.models import StakeholderTag,InstitutionTag,Factor,Question
from django.contrib.auth.models import User
from nameparser import HumanName
from django.db import transaction

@receiver(pre_save, sender=Institution)
def create_admin_for_institution(sender, instance, *args, **kwargs):
    if instance.id is None:
        #creating admin for institution
        username = instance._username
        full_name = instance._full_name
        email = instance._email
        password = instance._password

        name = HumanName(full_name)
        first_name = name.first
        last_name = name.last

        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

        instance.institution_admin = user


        #creating factors for institutions

@receiver(post_save, sender=Institution)
def create_factors_and_question_for_institution(sender, instance, created, *args, **kwargs):
    if created:
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

        with transaction.atomic():
            Student_Engagement = Factor(name="Student Engagement",description = "'Student engagement' assesses how effective the teacher is in creating a stimulating and interactive classroom environment that promotes active learning and student involvement.",institution = instance)
            Student_Engagement.save()
            Student_Engagement.institution_tag.add(tertiary)
            Student_Engagement.institution_tag.add(secondary)
            Student_Engagement.stakeholder_tag.add(student)

            question_1 = Question(question="Did your teacher encourage you to participate in class discussions and activities?",factor=Student_Engagement)
            question_1.save()
            question_1.stakeholder_tag.add(student)
            question_2 = Question(question="How often did your teacher use examples and stories to help you understand the lesson?",factor=Student_Engagement)
            question_2.save()
            question_2.stakeholder_tag.add(student)
            question_3 = Question(question="Did your teacher provide you with opportunities to work collaboratively with your peers?",factor=Student_Engagement)
            question_3.save()
            question_3.stakeholder_tag.add(student)
            question_4 = Question(question="Did your teacher make learning fun and enjoyable?",factor=Student_Engagement)
            question_4.save()
            question_4.stakeholder_tag.add(student)


            Learning_Outcomes = Factor(name="Learning Outcomes",description = "'Learning outcomes' assesses the extent to which the teacher has been successful in imparting knowledge and skills to the students and improving their academic performance.",institution = instance)
            Learning_Outcomes.save()
            Learning_Outcomes.institution_tag.add(tertiary)
            Learning_Outcomes.institution_tag.add(secondary)
            Learning_Outcomes.stakeholder_tag.add(student)

            question_5 = Question(question="How well does your teacher help you understand the material being taught?",factor = Learning_Outcomes)
            question_5.save()
            question_5.stakeholder_tag.add(student)
            question_6 = Question(question="How well does your teacher help you develop skills and knowledge that will prepare you for future academic and career success?",factor = Learning_Outcomes)
            question_6.save()
            question_6.stakeholder_tag.add(student)
            question_7 = Question(question="How well does your teacher create a positive and supportive learning environment that encourages you to take risks and learn from mistakes?",factor = Learning_Outcomes)
            question_7.save()
            question_7.stakeholder_tag.add(student)

            Classroom_Management = Factor(name="",description="",institution=instance)
            Communication_Skills = Factor(name="",description="",institution=instance)
            Professionalism = Factor(name="",description="",institution=instance)
            Collaboration = Factor(name="",description="",institution=instance)
            Planning_and_Preparation = Factor(name="",description="",institution=instance)
            Instructional_Planning = Factor(name="",description="",institution=instance)
            Instructional_Planning = Factor(name="",description="",institution=instance)

        
        


@receiver(pre_save, sender=Student)
def create_user_for_student(sender, instance, *args, **kwargs):
    if instance.id is None:
        first_name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        username = instance._student_username
        password = instance._student_password

        user = User(username=username, first_name=first_name, last_name=last_name, email = email)
        user.set_password(password)
        user.save()

        instance.user = user

@receiver(post_save, sender=Student)
def create_post_save_parent_for_student(sender, instance, created, *args, **kwargs):
    if created:
        parents_username = instance._parent_username
        phone_number = instance._parent_phone_number
        password = instance._parent_password

        user = User(username=parents_username)
        user.set_password(password)
        user.save()

        parent = Parent(user=user, phone_number=phone_number,institution = instance.institution,student = instance)
        parent.save()


@receiver(pre_save, sender=Teacher)
def create_user_for_teacher(sender, instance, *args, **kwargs):
    if instance.id is None:
        first_name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        username = instance._teacher_username
        password = instance._teacher_password

        user = User(username=username, first_name=first_name, last_name=last_name, email = email)
        user.set_password(password)
        user.save()

        instance.user = user