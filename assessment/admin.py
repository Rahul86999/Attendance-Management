from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Standard)
admin.site.register(Language)
#admin.site.register(LanuguageQuestions)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(QuestionHistory)
admin.site.register(Options)