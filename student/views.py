from django.shortcuts import render,redirect
from project_admin.models import AssignTest
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta,date
from django.http import HttpResponse
from assessment.models import QuestionCategory,Options,Question
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.views import View
# Create your views here.

@login_required
def student_home_view(request):
	
	#check whether user has old test which are not yet cancelled:
	#test = AssignTest.objects.filter(student__user=request.user,test_status='pending',test_datetime__lte=current_date_time)|AssignTest.objects.filter(elearning_stu__user=request.user,test_status='pending',test_datetime__lte=datetime.datetime.now())
	#test.update(test_status ='cancel')

	#current_date_time = date.strftime(datetime.datetime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	current_date_time = datetime.datetime.now().replace(microsecond=0)
	
	#fetch all upcoming test
	test = AssignTest.objects.filter(student__user=request.user,test_status__in=['pending','started'])|AssignTest.objects.filter(elearning_stu__user=request.user,test_status__in=['pending','started'])
	
	#if there are some upcoming test
	if test.count()>0:
		#check whether any test has already begun
		for t in test:
			#print(current_date_time + timedelta(days=0,minutes=int(t.duration)))
			print(t.test_datetime,type(t.test_datetime))
			print(current_date_time,type(current_date_time))
			
			test_end_time = t.test_datetime + timedelta(days=0,minutes=int(t.duration))
			
			#if test has begun
			if t.test_datetime <= current_date_time and t.test_datetime< test_end_time:
				
				remaining_minutes = (test_end_time -current_date_time ).seconds/60

				print('test duration',t.duration) #40
				print(remaining_minutes) #38
				#if only 10 minutes has passed
				if t.test_status == 'started' and test_end_time <= current_date_time:
					return redirect('start_test')

				if t.duration - remaining_minutes <=10 and remaining_minutes<= t.duration:
					t.test_status = 'started'
					t.save()
					return redirect('start_test')
					

				#if test missed
				else:
					t.test_status='cancel'
					t.save()

					
			if t.test_datetime<current_date_time:
				t.test_status='cancel'
				t.save()
				
		
		test = AssignTest.objects.filter(student__user=request.user,test_status__in=['pending','started'])|AssignTest.objects.filter(elearning_stu__user=request.user,test_status__in=['pending','started'])
		if test.count()>0:
			test1 = test.values('test_datetime').order_by('test_datetime')
			latest_test = test1[0]['test_datetime']
			print('A')
			return render(request,'student/home.html',{'test_date':latest_test,'count_upcoming':test.count()})

	
	return render(request,'student/home.html',{'test_date':'','count_upcoming':0})

@login_required
def start_test_view(request):

	test = AssignTest.objects.filter(student__user=request.user,test_status__in=['pending','started'])|AssignTest.objects.filter(elearning_stu__user=request.user,test_status__in=['pending','started'])
	test.order_by('test_datetime')

	if test.count()>=1:
		t = test.order_by('test_datetime')[0]	
	else:
		return redirect('student_home')

	print(test)
	return render(request,'student/test.html')

@login_required
def question_display_view(request):
	test = AssignTest.objects.filter(student__user=request.user,test_status='started')|AssignTest.objects.filter(elearning_stu__user=request.user,test_status='started')
	test.order_by('test_datetime')
	options_ans = request.POST.get('option')
	# print("answer============",options_ans)
	
	if test.count()==1:
		t = test.order_by('test_datetime')[0]
		print("test[0].test_paper",test[0].test_paper)
		options = Options.objects.filter(question__test=test[0].test_paper)
		
		return render(request,'student/english.html',{'options':options})
	else:
		return redirect('student_home')

class QuestionDisplay(View):
	def post(self,request):
		print("ajax")
		test = AssignTest.objects.filter(student__user=request.user,test_status='started')|AssignTest.objects.filter(elearning_stu__user=request.user,test_status='started')
		test.order_by('test_datetime')
		options_ans = request.POST.get('option')
		print("answer============",options_ans)
		answer_id = request.POST.get('answer_id')
		print("answer===answer_id=========",answer_id)
		option1 = "Transistor"
		if test.count()==1:
			t = test.order_by('test_datetime')[0]
			print("test[0].test_paper",test[0].test_paper)
			options = Options.objects.filter(question__test=test[0].test_paper)
			print("opionnjhfdbfhj",options)
			ans_match = options.filter(answer=options_ans)
			print("ans_match",ans_match)
			for i in ans_match:
				print("iiiii",i.id)
				answer_point = options.get(id=i.id)
				print("ans answer_point====",answer_point)
			incorect_value = 0.0
			corect_value = 0.0
			total = 0.0
			if ans_match:
				print("answer is correct")
				# messages.success(request, 'Answer is correct')
				corect = answer_point.ans_point
				corect_value = corect +1
				print("corect_value",corect_value)
				answer_point.ans_point = corect_value
				answer_point.save()
			else:
				ans_match = options.filter(option1=option1)
				print("ans_match  ifffffffff=",ans_match)
				for data in ans_match:
					print("eslse  iiiii",data.id)
					answer_point = options.get(id=data.id)
					print("========= answer_point====",answer_point)
					corect=answer_point.ans_point
					print("Incorrect answer, Try Again !")
					incorect_value = incorect_value - 0.25
					print("incorect_value",incorect_value)
					answer_point.ans_point = incorect_value + corect
					answer_point.save()
				# messages.warning(request, 'Incorrect answer, Try Again !')
			total = corect_value + incorect_value
			print("corect_value",corect_value,"incorect_value",incorect_value,"total=====",total)
			total2 = corect_value - incorect_value
			print("corect_value",corect_value,"incorect_value",incorect_value,"total2222==========",total2)
			data = total		
			return JsonResponse(data,safe=False)
		else:
			return JsonResponse({'status':'False'})

@login_required
def past_test_view(request):
	return render(request,'student/past_test.html')

@login_required
def upcoming_test_view(request):
	upcoming_test = AssignTest.objects.filter(student__user=request.user,test_status='pending')|AssignTest.objects.filter(elearning_stu__user=request.user,test_status='pending')
	return render(request,'student/upcoming_test.html',{'upcoming':upcoming_test,'count':upcoming_test.count()})

@login_required
def cancel_test_view(request,id):
	test = AssignTest.objects.get(id=id)
	test.test_status ='cancel'
	test.save()
	return redirect('upcoming_test')
