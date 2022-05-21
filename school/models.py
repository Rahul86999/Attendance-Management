from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


# class Test(models.Model):
# 	test_year = models.IntegerField(default=2020)
# 	quater = models.CharField(max_length=50,default='Quater1')
# 	subject_name = models.CharField(max_length=90,default='Embedded')
# 	test_duration  = models.PositiveIntegerField()
# 	package = models.CharField(max_length=50,default='p1')
# 	test_date = models.DateTimeField()
# 	created_at = models.DateTimeField(null=True,auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	standard = models.ForeignKey(Standard,on_delete=models.SET_NULL,null=True)
# 	created_by = models.ForeignKey(User,related_name = 'created_by',on_delete=models.SET_NULL,null=True)
# 	updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name = 'updated_by',null=True)




