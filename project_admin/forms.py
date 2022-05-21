from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
class SchoolReg(forms.ModelForm):

	class Meta:
		model = School
		fields='__all__' 
		exclude=('user','password')


class StudentReg(forms.ModelForm):

	class Meta:
		model=Student
		fields='__all__'
		exclude = ('user','password','school','assessment_given')

	def __init__(self,*args,**kwargs):
		school_id=kwargs.pop("school_id")
		super(StudentReg,self).__init__(*args,**kwargs)
		self.fields['teacher_assigned'].queryset=Teacher.objects.filter(school__id=school_id)



class TeacherReg(forms.ModelForm):

	class Meta:
		model=Teacher
		fields='__all__'
		exclude = ('user','password','school','assessment_given')

	
class IndividualStudentReg(UserCreationForm):
	class Meta :
		model = IndividualStudents
		fields = '__all__'
		exclude = ('user','password','assessment_given')


class AuthorityReg(forms.ModelForm):
	class Meta:
		model = AuthorityAccount
		fields ='__all__'
		exclude = ('user','password')