from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from stakeholder.models import Institution, Student, Parent,Teacher,Administrator
from evaluation.models import StakeholderTag,InstitutionTag,Factor,Question
from django.contrib.auth.models import User
from nameparser import HumanName
from django.db import transaction
from .utility import save_factors_for_institutions

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
            save_factors_for_institutions(instance)



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
        parents_username = instance.parent_username
        phone_number = instance.parent_phone_number
        password = instance.parent_password

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



@receiver(pre_save, sender=Administrator)
def create_user_for_administrator(sender, instance, *args, **kwargs):
    if instance.id is None:
        #creating user for institution
        username = instance._administrator_username
        email = instance._administrator_email
        password = instance._administrator_password
        first_name = instance.first_name
        last_name = instance.last_name

        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

        instance.user = user