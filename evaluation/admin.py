from django.contrib import admin
from .models import InstitutionTag,Factor,StakeholderTag, Question,EvaluationEvent,StudentEvaluationResponse,TeacherEvaluationResponse,ParentEvaluationResponse,AdministrationEvaluationResponse,SelfEvaluationResponse
# Register your models here.

admin.site.register(InstitutionTag)
admin.site.register(Factor)
admin.site.register(StakeholderTag)
admin.site.register(Question)
admin.site.register(EvaluationEvent)
admin.site.register(StudentEvaluationResponse)
admin.site.register(TeacherEvaluationResponse)
admin.site.register(ParentEvaluationResponse)
admin.site.register(AdministrationEvaluationResponse)
admin.site.register(SelfEvaluationResponse)