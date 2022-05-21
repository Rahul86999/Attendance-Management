from django.shortcuts import render,redirect,HttpResponse
from . form import *
from . models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import xlsxwriter
import xlrd
import io
import pandas as pd
# Create your views here.

def asse_index_view(request):
	if request.user.is_authenticated and request.user.user_type.role_name == 'Assessment': 
		return render(request,'assessment/index.html')

	else:
		return redirect('admin_login')


def create_test_view(request):
	if request.method=='POST':
		print('fsFDS');

	if request.user.is_authenticated and request.user.user_type.role_name == 'Assessment': 
		#english_form = AddQuestionForm()
		#hindi_form = AddQuestionForm()
		lang  = Language.objects.all()
		stand  = Standard.objects.all()

		return render(request,'assessment/add_test.html',{'lang':lang,'stand':stand})
	else:
		return redirect('admin_login')

@csrf_exempt
def add_basic_view(request):
	print("request test",request.POST)
	year = request.POST.get('year')
	quater = request.POST.get('quater')
	package = request.POST.get('package')
	test_name=request.POST.get('test_name')
	lang=request.POST.get('lang')
	date=request.POST.get('date')
	duration=request.POST.get('duration')
	standard=request.POST.get('standard')
	exam_no = request.POST.get('exam_no')
	print(duration)

	subject_dict={'P1':'Embedded','P2':'3D Printer','P3':'Mechanical','P4':'Safety Measureszzs','nonatl':'nonatl'}

	if str(exam_no) == "1":
		test = Test.objects.create(
			test_year = year,
			quater = quater,
			subject_name = subject_dict[package],
			test_duration = duration,
			package = package,
			test_date = date,
			standard_id = standard,
			created_by =request.user,
			updated_by = request.user
		)	

		for i in lang.split(','):
			TestLanguage.objects.create(
				test = test,
				test_lang = i
			)

	else:
		print(duration,'value')
		test = Test.objects.get(id=exam_no)
		test.test_year = year
		test.quater = quater
		test.subject_name = subject_dict[package]
		test.test_duration = duration
		test.package = package
		test.test_date = date
		test.standard_id = standard
		test.updated_by = request.user
		test.save()

		TestLanguage.objects.filter(test=test).delete()
		for i in lang.split(','):
			TestLanguage.objects.create(
				test = test,
				test_lang = i
			)
	
	return JsonResponse({'id':test.id})

@csrf_exempt
def add_category_view(request):
	exam_id  = request.POST.get('exam_id')
	cat_name  = request.POST.get('cat_name').split(',')
	max_mark  = request.POST.get('max_mark').split(',')
	no_question  = request.POST.get('no_question').split(',')
	cat_id = request.POST.get('cat_id').split(',')

	c_id=''
	print(exam_id)
	for i in range(1,len(cat_name)):
		if str(cat_id[i])!='1':
			qc = QuestionCategory.objects.get(id=cat_id[i])
			qc.category_name = cat_name[i]
			qc.question_to_deliver = no_question[i]
			qc.max_score = max_mark[i]
			qc.updated_by = request.user
			qc.save()
		else:
			q = QuestionCategory.objects.create(
				test_id=exam_id,
				category_name = cat_name[i],
				question_to_deliver = no_question[i],
				max_score = max_mark[i],
				created_by = request.user
			)
			c_id+=str(q.id)+','
	
	return JsonResponse({'cat_id':c_id})

def edit_test_view(request):
	test = Test.objects.all()
	return render(request,'assessment/edit_test.html',{'test':test})


def delete_test_view(request,id):
	obj = Test.objects.get(id=id)
	obj.delete()
	return redirect('edit_test')

def edit_test_details_view(request,id):
	test = Test.objects.get(id=id)
	lang  = Language.objects.all()
	stand  = Standard.objects.all()

	selected_lang=TestLanguage.objects.filter(test=test).values('test_lang')
	return render(request,'assessment/edit_test_details.html',{'test':test,'lang':lang,'stand':stand,
		'selected_lang':selected_lang})


@csrf_exempt
def add_question_view(request):
	question = request.POST.get('question')
	level = request.POST.get('level')
	quest_type =request.POST.get('quest_type')
	options = request.POST.get('options')
	answer = request.POST.get('answer')
	exam_id = request.POST.get('exam_id')
	category = request.POST.get('category')
	print('Exam id is',answer,options)
	ques = Question.objects.create(
		question_category=QuestionCategory.objects.get(test__id=exam_id,category_name=category),
		test=Test.objects.get(id=exam_id),
		language = Language.objects.get(lang_name='Hindi'),
		question_title = question,
		question_tags = quest_type,
		level =level,
		updated_by= request.user

		)
	o = Options.objects.filter(question=ques).delete()
	opt = options.split(',')
	ans =[i for i in  answer.split(',')[:len(answer)-1]]
	print(ans)
	for i in range(len(opt)-1):
		if str(i) in ans:
			Options.objects.create(question=ques,answer=opt[i],is_valid=True)
		else:
			Options.objects.create(question=ques,answer=opt[i],is_valid=False)


	data =dict()
	qestions = Question.objects.filter(test__id=exam_id)
	option = Options.objects.filter(question=qestions[0])
	data['content'] = render_to_string('assessment/partial/partial-table.html', {'qestions':qestions,'option':option})
	return JsonResponse(data)


@csrf_exempt
def add_question_passage_view(request):
	question = request.POST.get('question')
	level= request.POST.get('level')
	quest_type = request.POST.get('quest_type')
	exam_id = request.POST.get('exam_id')
	category = request.POST.get('category')
	print(category)
	print(exam_id)
	print(question)
	ques = Question.objects.create(
		question_category=QuestionCategory.objects.get(test__id=exam_id,category_name=category),
		test=Test.objects.get(id=exam_id),
		language = Language.objects.get(lang_name='Hindi'),
		question_title = question,
		question_tags = quest_type,
		level =level,
		updated_by= request.user
		)	

	data =dict()
	qestions = Question.objects.filter(test__id=exam_id)
	option = Options.objects.filter(question=qestions[0])
	data['content'] = render_to_string('assessment/partial/partial-table.html', {'qestions':qestions,'option':option})
	return JsonResponse(data)


def download_sample_excel_view(request):
	
	exam_id = request.GET.get('exam_id')
	cat = QuestionCategory.objects.filter(test_id = exam_id)
	category = [i.category_name for i in cat]
	output = io.BytesIO()# Create an in-memory output file for the new workbook.
	

	workbook = xlsxwriter.Workbook(output) #write
	worksheet = workbook.add_worksheet()
	data = ['Category','Question Title','Level(Easy/Medium/Difficult)','Question Type(Single Correct/Multiple Correct)','Options separated with ;','Correct Answer sepatreted with;']
	text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','bold': True})
	row = 0
	col = 0

	for i in data:
		worksheet.write(row,col,i,text_format)
		col+=1
	worksheet.data_validation(1,2,10000,2,{'validate':'list','source':['Easy','Medium','Difficult']})
	worksheet.data_validation(1,3,10000,3,{'validate':'list','source':['Single Correct','Multiple Correct','Passage Based']})
	worksheet.data_validation(1,0,10000,0,{'validate':'list','source':category})


	workbook.close()   
	
	output.seek(0)
	#worksheet4.filter_column('C'
	#worksheet.data_validation(1,3,1000,3, {'validate': 'list','source': ['Easy', 'Medium', 'Difficult']})
	filename='sample.xlsx'
	response = HttpResponse(output,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

@csrf_exempt
def excel_upload_view(request):

	exam_id = request.POST.get('exam_no')
	excel_file = request.FILES['xlsx']
	data =dict()
	df=pd.read_excel(excel_file,header=0)
	q_type={'Single Correct':'Single','Multiple Correct':'Multiple','Passage Based':'Passage'}

	if len(df.values)>0:	
		for row in df.values:
			q=Question.objects.create(
				question_category = QuestionCategory.objects.get(test_id=exam_id,category_name=row[0]),
				test=Test.objects.get(id=exam_id),
				question_title = row[1],
				question_tags = q_type[row[3]],
				level =row[2],
				updated_by = request.user

			)
			if q.question_type in ['Single','Multiple']:
				answer = row[5].split(';')
				for i in row[4].split(';'):
					if i in answer:
						Options.objects.create(question=q,answer=i,is_valid=True)
					else:
						Options.objects.create(question=q,answer=i,is_valid=False)
	
	qestions = Question.objects.filter(test_id=exam_id)
	option = Options.objects.filter(question=qestions[0])
	data['content'] = render_to_string('assessment/partial/partial-table.html', {'qestions':qestions,'option':option})
	return JsonResponse(data)



def del_quest_view(request):
	id=request.GET.get('id')
	exam_id=request.GET.get('exam_id')

	Question.objects.filter(id=id).delete()
	data =dict()
	qestions = Question.objects.filter(test__id=exam_id)
	if (qestions.count()==0):
		option={}
	else:
		option = Options.objects.filter(question=qestions[0])
	data['content'] = render_to_string('assessment/partial/partial-table.html', {'qestions':qestions,'option':option})
	return JsonResponse(data)