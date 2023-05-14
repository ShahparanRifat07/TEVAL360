from django.contrib import admin
from .models import Institution,Student,Parent,Department,Teacher,Course,Administrator
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Student)
class StudentModelAdmin(ImportExportModelAdmin):
    list_display = ('first_name','last_name','student_id','email')


admin.site.register(Institution)

admin.site.register(Parent)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Administrator)
admin.site.register(Course)