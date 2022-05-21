from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
from assessment.models import Test,Question


# Create your models here.
class AffiliationType(models.Model):
	affiliation_name = models.CharField(max_length=200)

	def __str__(self):
		return self.affiliation_name

class School(models.Model):

	user=models.ForeignKey(User,null=True,related_name="school_pro",on_delete=models.SET_NULL)
	school_name = models.CharField(max_length=50)
	password=models.CharField(max_length=40)
	email=models.EmailField()
	phone=models.BigIntegerField()
	address = models.TextField()
	school_board = models.ForeignKey(AffiliationType,on_delete=models.SET_NULL,null=True)
	incharge_name = models.CharField(max_length=90,null=True)
	incharge_email =models.EmailField(null=True)

	def __str__(self):
		return self.school_name

s=(('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'))


class Teacher(models.Model):
	user=models.ForeignKey(User,null=True,related_name="teacher",on_delete=models.SET_NULL)
	school = models.ForeignKey(School,related_name="teacher",on_delete=models.CASCADE)
	teacher_name = models.CharField	(max_length=40)
	enrollment_no = models.CharField(max_length=100)
	password=models.CharField(max_length=40)
	email=models.EmailField()
	phone=models.BigIntegerField()
	address = models.TextField()
	assessment_given = models.IntegerField(default = 0)

	def __str__(self):
		return self.teacher_name

class Student(models.Model):
	
	user=models.ForeignKey(User,null=True,related_name="student",on_delete=models.SET_NULL)
	school = models.ForeignKey(School,related_name="student",on_delete=models.CASCADE)
	student_name = models.CharField	(max_length=40)
	enrollment_no = models.CharField(max_length=100)
	password=models.CharField(max_length=40)
	email=models.EmailField()
	phone=models.BigIntegerField()
	address = models.TextField()
	standard = models.CharField	(max_length=10,choices=s)
	assessment_given = models.IntegerField(default = 0)
	teacher_assigned = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True)
	
	def __str__(self):
		return self.student_name


class IndividualStudents(models.Model):
	user=models.ForeignKey(User,null=True,related_name="individual_student",on_delete=models.SET_NULL)
	student_name = models.CharField(max_length=70)
	student_email = models.EmailField()
	student_phone = models.BigIntegerField()
	address = models.TextField()
	course_pursuing = models.CharField(max_length=100,null=True)
	password=models.CharField(max_length=40)
	current_institution_name = models.CharField(max_length=50,null=True)
	assessment_given = models.IntegerField(default = 0)
	student_type = models.CharField(max_length=30,choices=(('ATL','ATL'),('Non ATL','Non ATL')),default='ATL')

	def __str__(self):
		return self.student_name


class SchoolAssignedTestPaper(models.Model):
	test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
	students = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
	school  = models.ForeignKey(School,on_delete=models.SET_NULL,null=True)
	duration = models.IntegerField()
	start_time = models.DateTimeField()

class IndividualTestPaper(models.Model):
	test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
	student  = models.ForeignKey(IndividualStudents,on_delete=models.SET_NULL,null=True)
	duration = models.IntegerField()
	start_time = models.DateTimeField()


class AuthorityAccount(models.Model):
	auth_type = (
		('CBSE Authority','CBSE Authority'),
		('Niti Aayog','Niti Aayog'),
		('State Eductaion','State Eductaion'),
		('Cooperation','Cooperation'),
	)
	user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
	email = models.EmailField(null=True)
	employee_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	phone = models.BigIntegerField()
	password = models.CharField(max_length=40)
	designation = models.CharField(max_length=100)
	government  = models.CharField(max_length=50)
	authority_type = models.CharField(max_length=60,choices=auth_type)


class AssignTest(models.Model):
	stype=(
		('School Student','School Student'),
		('e-learning Student','e-learning Student')
	)
	student_type = models.CharField(max_length=30,choices=stype)
	school = models.ForeignKey(School,on_delete=models.SET_NULL,null=True)
	student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
	stu_class = models.CharField(max_length=50,null=True)
	test_paper = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
	duration  = models.FloatField()
	test_datetime = models.DateTimeField()
	test_appeared = models.BooleanField(default=False)
	elearning_stu = models.ForeignKey(IndividualStudents,on_delete=models.SET_NULL,null=True)
	test_status = models.CharField(max_length=60,default="pending")

class StudentTestPaper(models.Model):
	student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
	elearning_stu = models.ForeignKey(IndividualStudents,on_delete=models.SET_NULL,null=True)
	assigned_test = models.ForeignKey(AssignTest,on_delete=models.SET_NULL,null=True)
	marks = models.IntegerField()
	attempt = models.IntegerField()
	question = models.ForeignKey(Question,on_delete=models.SET_NULL,null=True)
	