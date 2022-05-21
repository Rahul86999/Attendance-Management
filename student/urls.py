from django.urls import path
from . import views

urlpatterns = [
	path('student/home/',views.student_home_view,name='student_home'),
	path('student/Test/',views.past_test_view,name='past_test'),
	path('upcoming/Test/',views.upcoming_test_view,name='upcoming_test'),
	path('cancel/Test/<int:id>',views.cancel_test_view,name='cancel_test'),
	path('start/Test/',views.start_test_view,name='start_test'),
	path('assessment/',views.question_display_view,name='display_question'),
	path('question/display/',views.QuestionDisplay.as_view(),name='question_ans_display'),
	
]