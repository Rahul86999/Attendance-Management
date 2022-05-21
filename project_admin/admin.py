from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(AffiliationType)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Teacher)


class AssignTestAdmin(admin.ModelAdmin):
	list_display = ['student_type','school','student','test_paper','duration','test_datetime','test_appeared','elearning_stu']

admin.site.register(AssignTest,AssignTestAdmin)