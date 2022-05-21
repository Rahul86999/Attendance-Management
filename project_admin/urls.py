
from django.urls import path
from . import views

urlpatterns = [

	path('',views.admin_index_view,name='admin_index'),
	path('Assessment/Manage',views.assessment_manage_view,name='assess_manage'),
	path('login/',views.admin_login_view,name='admin_login'),
	path('Authority/Manage',views.authority_manage_view,name='authority_manage'),

	path('School/Manage',views.school_manage_view,name='school_manage'),
	path('Individual/studnet/',views.add_individual_student_view,name  = 'add_individual_student'),
	


	path('detail/school/<int:id>',views.detail_school_view,name='detail_school'),

	path('add/student/<int:id>',views.add_student_view,name='add_student'),
	path('add/teacher/<int:id>',views.add_teacher_view,name='add_teacher'),


	path('student/list/<int:id>',views.student_list_view,name='student_list'),
	path('teacher/list/<int:id>',views.teacher_list_view,name='teacher_list'),

	path('upload_excel/<int:id>',views.student_upload_view,name='upload_excel_student'),
	path('Test/Assign/<int:id>',views.test_assign_view,name='test_paper_assign'),
	

	path('Assign/Paper',views.assign_test_paper,name="assign_test_paper"),


	path('change-password/',views.change_password,name='change_password'),
	
	path('get/School/',views.get_school_view,name='get_school'),
	path('get/Class/',views.get_class_view,name='get_class'),
	path('get/Student/',views.get_student_view,name='get_student'),
	path('get/e-learning/student/',views.e_learning_stu,name='e-learn-stu'),
	path('check/available/',views.paper_available_view,name='check_available'),

]