from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.
class Standard(models.Model):
	standard_name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.standard_name
	
class Language(models.Model):
	lang_name = models.CharField(max_length=30)

	def __str__(self):
		return self.lang_name

#class Subject(models.Model):
#	sub_name = models.CharField(max_length=40)

class Test(models.Model):
	test_year = models.IntegerField(default=2020)
	quater = models.CharField(max_length=50,default='Quater1')
	subject_name = models.CharField(max_length=90,default='Embedded')
	test_duration  = models.PositiveIntegerField()
	package = models.CharField(max_length=50,default='p1')
	test_date = models.DateTimeField()
	created_at = models.DateTimeField(null=True,auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	standard = models.ForeignKey(Standard,on_delete=models.SET_NULL,null=True)
	created_by = models.ForeignKey(User,related_name = 'created_by',on_delete=models.SET_NULL,null=True)
	updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name = 'updated_by',null=True)


class TestLanguage(models.Model):
	test = models.ForeignKey(Test,on_delete=models.CASCADE)
	test_lang= models.CharField(max_length=50)
	created_at = models.DateTimeField(null=True,auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class QuestionCategory(models.Model):

	test = models.ForeignKey(Test,on_delete=models.CASCADE)
	category_name = models.CharField(max_length=50)
	question_to_deliver = models.IntegerField()
	max_score = models.IntegerField()
	created_at = models.DateTimeField(null=True,auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User,related_name = 'cat_created_by',on_delete=models.SET_NULL,null=True)
	updated_by = models.ForeignKey(User,related_name = 'cat_updated_by',on_delete=models.SET_NULL,null=True)


class Question(models.Model):
	question_category =  models.ForeignKey(QuestionCategory,on_delete=models.SET_NULL,null=True)
	test = models.ForeignKey(Test,on_delete=models.CASCADE)
	question_type= (
		('Single Correct','Single'),
		('Multiple Correct','Multiple'),
		('Passage Based','Passage')
	)

	language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)
	question_title = models.TextField(default='')
	question_tags = models.CharField(max_length=60,choices=question_type,default="Single")
	level = models.CharField(max_length=50,default="Easy",choices=(('Easy','Easy'),('Medium','Medium'),('Difficult','Difficult')))
	created_at = models.DateTimeField(null=True,auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

class Options(models.Model):
	question = models.ForeignKey(Question,related_name='options',on_delete=models.CASCADE)
	answer = models.CharField(max_length=1000)
	option1 = models.CharField(max_length=500,null=True,blank=True)
	option2 = models.CharField(max_length=500,null=True,blank=True)
	option3 = models.CharField(max_length=500,null=True,blank=True)
	option4 = models.CharField(max_length=500,null=True,blank=True)
	is_valid = models.BooleanField()
	ans_point = models.FloatField(null=True, blank=True, default=0)


class QuestionHistory(models.Model):
	test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
	updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
	created_at = models.DateTimeField(null=True,auto_now_add=True)


