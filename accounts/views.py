from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from project_admin.models import *
from accounts.forms import SignUpForm
# Create your views here.
def index_view(request):
	return render(request,'common/index.html')


def choose_reg_view(request):
	return render(request,'common/chooseschoolreg.html')


def atl_school_reg_view(request):
	return render(request,'common/schoolreg.html')


def cbse_reg_view(request):
	return render(request,'common/inchargecbse.html')	


def school_atl_incharge_view(request):
	return render(request,'common/incharge.html')


def vendor_reg_view(request):
	return render(request,'common/vendor.html')

def lab_reg_view(request):
	return render(request,'common/regi.html')



def mentor_change_view(request):
	return render(request,'common/mentorofchange.html')

def authority_dash_view(request):
	return render(request,'common/authority.html')


def assessment_view(request):
	return render(request,'common/atlcbse.html')
	

def logout_admin_view(request):
	logout(request)
	return redirect('admin_index')


def login_view(request):
	username  = request.POST.get('username')
	password = request.POST.get('password')

	user = authenticate(username=username,password=password)
	if user is not None:
		login(request,user)
		if request.user.user_type.role_name == 'Admin':
			return redirect('admin_index')
		elif request.user.user_type.role_name == 'Assessment':
			print('A')
			return redirect('assessment_index')
	else:
		messages.error(request, 'Invalid Username or password!')  
		#previous_page=request.META['HTTP_REFERER']
		print('dsafs')

		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cbse_login_view(request):
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		schoolid = request.POST.get('schoolid')

		if request.POST.get('type') =='Teacher':
			teacherid = request.POST.get('teacherid')
			if (Teacher.objects.filter(user__username = username, school_id = schoolid,id=teacherid).count() ==1):
				print(username,password)
				user  = authenticate(username=username,password=password)
				print(user)
				if user!=None:
					login(request,user)
					messages.success(request, 'Login Successful!')
					return redirect('cbse_login')
				else:
					messages.error(request, 'Invalid username or passsword!')
					return redirect('cbse_login')  

			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('cbse_login')  

		else:
			studentid = request.POST.get('studentid')
			print(studentid)
			if (Student.objects.filter(user__username = username, school_id = schoolid,id=studentid).count() ==1):
				user  = authenticate(username=username,password=password)
				if user!=None:
					login(request,user)
					messages.success(request, 'Login Successful!')
					return redirect('student_home')
				else:
					messages.error(request, 'Invalid username or passsword!')
					return redirect('cbse_login')  

			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('cbse_login')
	else:
		return render(request,'common/cbselogin.html')



def atl_login_view(request):
	print("req",request.POST)
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		schoolid = request.POST.get('schoolid')

		if request.POST.get('type') =='Teacher':
			teacherid = request.POST.get('teacherid')
			ab= Teacher.objects.filter(user__username = username, school_id = schoolid,id=teacherid)
			print("teacher",ab)
			if (Teacher.objects.filter(user__username = username, school_id = schoolid,id=teacherid).count() ==1):
				print(username,password)
				user  = authenticate(username=username,password=password)
				print(user)
				if user!=None:
					login(request,user)
					messages.success(request, 'Login Successful!')
					return redirect('atl_login')
				else:
					messages.error(request, 'Invalid username or passsword!')
					return redirect('atl_login')  

			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('atl_login')  

		else:
			studentid = request.POST.get('studentid')
			print(studentid)
			if (Student.objects.filter(user__username = username, school_id = schoolid,id=studentid).count() ==1):
				user  = authenticate(username=username,password=password)
				if user!=None:
					login(request,user)
					messages.success(request, 'Login Successful!')
					return redirect('student_home')
				else:
					messages.error(request, 'Invalid username or passsword!')
					return redirect('atl_login')  

			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('atl_login')

	return render(request,'common/atllogin.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('atl_login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})