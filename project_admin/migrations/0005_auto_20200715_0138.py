# Generated by Django 3.0.7 on 2020-07-14 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0004_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='standard',
            field=models.CharField(choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=10),
        ),
    ]
