
from django.urls import path
from . import views

urlpatterns = [
	path('assessment/Dashboard/',views.asse_index_view,name='assessment_index'),
	path('Create/Test/',views.create_test_view,name='add_test'),
	path('Add/basic/',views.add_basic_view,name='add_basic'),
	path('Add/Category/',views.add_category_view,name='add_category'),
	path('Edit/Test/',views.edit_test_view,name='edit_test'),
	path('delete/test/<int:id>',views.delete_test_view,name='delete_test'),
	path('edit/test/<int:id>',views.edit_test_details_view,name='edit_test_details'),
	path('add/question/',views.add_question_view,name='add_question'),
	path('add/question/passage/',views.add_question_passage_view,name='add_passage_question'),

	path('Sample/Excel/',views.download_sample_excel_view,name='download_sample_excel'),
	path('Upload/Excel/',views.excel_upload_view,name='excel_uploads'),

	path('delete/Question/',views.del_quest_view,name='del_quest')
]
