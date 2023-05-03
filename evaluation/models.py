from django.db import models
from stakeholder.models import Institution,Department,Teacher,Student,Parent,Course,Administrator
from django.utils import timezone

# Create your models here.


class StakeholderTag(models.Model):
    name=models.CharField(max_length=64)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class InstitutionTag(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Factor(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True,null=True)
    institution_tag = models.ManyToManyField(InstitutionTag)
    stakeholder_tag = models.ManyToManyField(StakeholderTag)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField()
    stakeholder_tag = models.ManyToManyField(StakeholderTag)
    institution_tag = models.ManyToManyField(InstitutionTag)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    # institution = models.ForeignKey(Institution,on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class EvaluationEvent(models.Model):
    name = models.CharField(max_length=128,null=True,blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    stakeholder_tag = models.ManyToManyField(StakeholderTag)
    student_factor = models.ManyToManyField(Factor, related_name="evaluation_student_factor",blank=True)
    parent_factor = models.ManyToManyField(Factor, related_name="evaluation_parent_factor",blank=True)
    teacher_factor = models.ManyToManyField(Factor, related_name="evaluation_teacher_factor",blank=True)
    self_factor = models.ManyToManyField(Factor, related_name="evaluation_self_factor",blank=True)
    administrator_factor = models.ManyToManyField(Factor, related_name="evaluation_administrator_factor",blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    event_created = models.DateTimeField(default=timezone.now)
    is_end = models.BooleanField(default=False)
    is_start = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = self.institution.institution_name+"["+ str(self.start_date) +"-"+str(self.end_date)+"]"
            super().save(*args, **kwargs)



class StudentEvaluationResponse(models.Model):
    evaluaton_event = models.ForeignKey(EvaluationEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question.id)+" /"+self.student.first_name+" /"+str(self.evaluaton_event.id)+" /"+self.teacher.first_name
    


class TeacherEvaluationResponse(models.Model):
    evaluaton_event = models.ForeignKey(EvaluationEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="evaluator")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question.id)+" /"+self.evaluator.first_name+" /"+str(self.evaluaton_event.id)+" /"+self.teacher.first_name
    


class ParentEvaluationResponse(models.Model):
    evaluaton_event = models.ForeignKey(EvaluationEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question.id)+" /"+self.parent.student.first_name+" /"+str(self.evaluaton_event.id)+" /"+self.teacher.first_name
    


class AdministrationEvaluationResponse(models.Model):
    evaluaton_event = models.ForeignKey(EvaluationEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question.id)+" /"+self.administrator.first_name+" /"+str(self.evaluaton_event.id)+" /"+self.teacher.first_name
    



class SelfEvaluationResponse(models.Model):
    evaluaton_event = models.ForeignKey(EvaluationEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question.id)+" /"+self.teacher.first_name+" /"+str(self.evaluaton_event.id)