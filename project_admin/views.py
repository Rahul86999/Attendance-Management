from django.shortcuts import render,redirect
from accounts.models import Roles
# Create your views here.
from accounts.forms import SignUpForm
from django.contrib.auth import get_user_model
from . forms import *
import string
import random
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from assessment.models import Test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test


User = get_user_model()
letters_and_digits = string.ascii_letters + string.digits


def admin_login_view(request):
	return render(request,'project_admin/login.html')

def admin_index_view(request):
	
	if request.user.is_authenticated and request.user.is_superuser:
		return render(request,'project_admin/dashboard.html')

	else:
		return redirect('admin_login')


@user_passes_test(lambda u: u.is_superuser)
def assessment_manage_view(request):
	if request.method=='POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.user_type=Roles.objects.get(role_name ='Assessment' )
			form.save()
			return redirect('assess_manage')
		else:
			return render(request,'project_admin/assessment_manage.html',{'form':form,'error':'error'})
	else:
		users = User.objects.filter(user_type__role_name='Assessment')
		form = SignUpForm()
		return render(request,'project_admin/assessment_manage.html',{'form':form,'users':users})


@user_passes_test(lambda u: u.is_superuser)
def school_manage_view(request):
	letters_and_digits = string.ascii_letters + string.digits

	if request.method == 'POST':
		random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
		form = SchoolReg(request.POST)
		sc_name = request.POST['school_name']
		if form.is_valid():
			user_count = User.objects.filter(first_name__iexact=sc_name).count()
			if (user_count == 0):
				user = User.objects.create(username=sc_name,password=random_str,first_name=sc_name,user_type=Roles.objects.get(role_name='School'))
			else:
				user = User.objects.create(username=sc_name+str(user_count+1),password=random_str,first_name=sc_name,user_type=Roles.objects.get(role_name='School'))

			form = form.save(commit=False)
			form.password=random_str
			form.user = user
			form.save()
		messages.success(request,'School Added Successfully')
		return redirect('school_manage')
	else:
		form = SchoolReg()
		school = School.objects.all()
		return render(request,'project_admin/school_manage.html',{'form':form,'school':school})


@user_passes_test(lambda u: u.is_superuser)
def detail_school_view(request,id):
	return render(request,'project_admin/school_detail.html',{'id':id})


@user_passes_test(lambda u: u.is_superuser)
def add_student_view(request,id):
	if request.method == 'POST':
		random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
		form = StudentReg(request.POST,school_id=id)
		stu_name = request.POST.get('student_name')

		if form.is_valid():
			user_count = User.objects.filter(first_name__iexact=stu_name).count()

			if (user_count == 0):
				user = User.objects.create_user(username=stu_name,password=random_str,first_name=stu_name,user_type=Roles.objects.get(role_name='Student'))
			else:
				user = User.objects.create_user(username=stu_name+str(user_count+1),password=random_str,first_name=stu_name,user_type=Roles.objects.get(role_name='Student'))

			form = form.save(commit=False)
			form.password=random_str
			form.school_id=id
			form.user = user
			form.save()
			messages.success(request,'Student Added Successfully')
			return redirect('student_list',id)
		else:
			
			return render(request,'project_admin/createstudent.html',{'id':id,'form':form})
	else:
		form = StudentReg(school_id=id)
		return render(request,'project_admin/createstudent.html',{'id':id,'form':form})


@user_passes_test(lambda u: u.is_superuser)
def add_teacher_view(request,id):
	if request.method == 'POST':
		random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
		form = TeacherReg(request.POST)
		teac_name = request.POST.get('teacher_name')

		if form.is_valid():
			user_count = User.objects.filter(first_name__iexact=teac_name).count()

			if (user_count == 0):
				user = User.objects.create_user(username=teac_name,password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='Teacher'))
			else:
				user = User.objects.create_user(username=teac_name+str(user_count+1),password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='Teacher'))

			form = form.save(commit=False)
			form.password=random_str
			form.school_id=id
			form.user = user
			form.save()
			messages.success(request,'Teacher Added Successfully')
			return redirect('teacher_list',id)
		else:
			
			return render(request,'project_admin/createstudent.html',{'id':id,'form':form})
	else:
		form = TeacherReg()
		return render(request,'project_admin/createstudent.html',{'id':id,'form':form})

@user_passes_test(lambda u: u.is_superuser)
def add_individual_student_view(request):
	if request.method == 'POST':
		random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
		form = IndividualStudentReg(request.POST)
		teac_name = request.POST.get('student_name')

		if form.is_valid():
			user_count = User.objects.filter(username__iexact=teac_name).count()

			if (user_count == 0):
				user = User.objects.create_user(username=teac_name,password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='Student'))
			else:
				user = User.objects.create_user(username=teac_name+str(user_count+1),password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='StudentReg'))

			form = form.save(commit=False)
			form.password=random_str
			form.school_id=id
			form.user = user
			form.save()
			messages.success(request,'Student Added Successfully')
			return redirect('add_individual_student')
		else:
			
			return render(request,'project_admin/createstudent.html',{'id':id,'form':form})
	else:
		form = IndividualStudentReg()
		stu = IndividualStudents.objects.all()
		return render(request,'project_admin/individual_student_list.html',{'stu':stu,'form':form})


@user_passes_test(lambda u: u.is_superuser)
def student_list_view(request,id):
	stu = Student.objects.filter(school_id=id)
	print(stu)
	return render(request,'project_admin/student_list.html',{'stu':stu,'id':id})


@user_passes_test(lambda u: u.is_superuser)
def teacher_list_view(request,id):
	teacher = Teacher.objects.filter(school_id=id)
	print(teacher)
	return render(request,'project_admin/teacher_list.html',{'teacher':teacher,'id':id})	


@user_passes_test(lambda u: u.is_superuser)
def student_upload_view(request,id):
	pass

@user_passes_test(lambda u: u.is_superuser)
def test_assign_view(request,id):
	standard = Student.objects.all().values('standard').distinct()
	return render(request,'project_admin/stu_test_assign.html',{'standard':standard,'id':id})
	

@user_passes_test(lambda u: u.is_superuser)	
def authority_manage_view(request):
	if request.method=='POST':
		random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
		form = AuthorityReg(request.POST)
		teac_name = request.POST.get('employee_name')

		if form.is_valid():
			user_count = User.objects.filter(username__iexact=teac_name).count()

			if (user_count == 0):
				user = User.objects.create_user(username=teac_name,password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='Authority'))
			else:
				user = User.objects.create_user(username=teac_name+str(user_count+1),password=random_str,first_name=teac_name,user_type=Roles.objects.get(role_name='Authority'))

			form = form.save(commit=False)
			form.password=random_str
			form.school_id=id
			form.user = user
			form.save()
			messages.success(request,'Authority account created Successfully')
			return redirect('authority_manage')
		
	else:
		users = AuthorityAccount.objects.all()
		form= AuthorityReg()
		return render(request,'project_admin/authoity_manage.html',{'form':form,'users':users})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'project_admin/change_password.html', {
        'form': form
    })

@user_passes_test(lambda u: u.is_superuser)
def assign_test_paper(request):
	if request.method == 'POST':
		stype = request.POST.get('wise')
		sc_name = request.POST.get('sc_name')
		no_students  = request.POST.get('no_students')
		stu_name = request.POST.getlist('stu_name')
		year = request.POST.get('year')
		paper_standard = request.POST.get('paper_standard')
		quater = request.POST.get('quater')
		package = request.POST.get('package')
		date = request.POST.get('date')
		duration = request.POST.get('duration')
		st_class = request.POST.get('st_class')
		print(stu_name)
			
		papers = Test.objects.filter(test_year=year,package = package,standard__standard_name=paper_standard,quater=quater)
		
		if papers.count() >= 1:
			if stype == 'School Student':
				if no_students == 'all_student':
					sc = Student.objects.filter(school_id=sc_name,standard=st_class)
					for stu in sc:
						past_assigned = AssignTest.objects.filter(student=stu,test_paper=papers[0],test_appeared=False)
						if (past_assigned.count()==1):
							past_assigned.update(duration =duration,test_datetime=date)						
							
						else:
							AssignTest.objects.get_or_create(student_type = stype,student=stu,school_id=sc_name,stu_class=st_class,test_paper=papers[0],duration=duration,test_datetime=date)

				elif no_students == 'selectstu':
					for i in stu_name:
						past_assigned = AssignTest.objects.filter(student_id=i,test_paper=papers[0],test_appeared=False)
						if (past_assigned.count()==1):
							past_assigned.update(duration =duration,test_datetime=date)						
							
						else:
							AssignTest.objects.get_or_create(student_type = stype,student_id=i,school_id=sc_name,stu_class=st_class,test_paper=papers[0],duration=duration,test_datetime=date)
				messages.success(request,'Test Paper Assigned')
			# assign test paper to e-learning students
			if stype=='e-learning Student':
				past_assigned = AssignTest.objects.filter(elearning_stu_id=sc_name,test_paper=papers[0],test_appeared=False)
				if (past_assigned.count()==1):
					past_assigned.update(duration =duration,test_datetime=date)						
							
				else:
					AssignTest.objects.get_or_create(student_type = stype,elearning_stu_id=sc_name,test_paper=papers[0],duration=duration,test_datetime=date)
			
				messages.success(request,'Test Paper Assigned')

				
				return redirect('assign_test_paper')		

		else:
			messages.error(request,'Test Paper Not Available')
			return redirect('assign_test_paper')
	else:
		year = Test.objects.values('test_year').distinct()
		return render(request,'project_admin/assignTestPaper.html',{'year':year})


@user_passes_test(lambda u: u.is_superuser)
def get_school_view(request):
	school = list(School.objects.values('id','school_name'))
	return JsonResponse(school,safe=False)

@user_passes_test(lambda u: u.is_superuser)
def get_class_view(request):
	school_id = request.GET.get('id')
	standard = list(Student.objects.filter(school_id=school_id).values('standard').distinct())

	return JsonResponse(standard,safe=False)

@user_passes_test(lambda u: u.is_superuser)
def get_student_view(request):
	name = request.GET.get('name')
	class_name = request.GET.get('class')

	stu = list(Student.objects.filter(school_id=name,standard=class_name).values('id','student_name'))
	return JsonResponse(stu,safe=False)

@user_passes_test(lambda u: u.is_superuser)
def e_learning_stu(request):
	indstu = list(IndividualStudents.objects.values('id','student_name'))
	return JsonResponse(indstu,safe=False)

@csrf_exempt
def paper_available_view(request):
	year = request.POST.get('year')
	standard = request.POST.get('paper_standard')
	quater = request.POST.get('quater')
	package = request.POST.get('package')

	papers = Test.objects.filter(test_year=year,package = package,standard__standard_name=standard,quater=quater)
						
						#)#standard__name=standard,
	print(papers)
	if papers.count() >= 1:
		return JsonResponse({'status':'Available'})
	else:
		return JsonResponse({'status':'Not Available'})