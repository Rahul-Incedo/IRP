# Generated by Django 3.1.5 on 2021-02-02 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('f_name', models.CharField(max_length=64)),
                ('m_name', models.CharField(blank=True, max_length=64, null=True)),
                ('l_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('CGPA', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('college_name', models.CharField(max_length=254)),
                ('experience', models.IntegerField(null=True)),
                ('mobile', models.CharField(max_length=10)),
                ('DOB', models.DateField(auto_now=True)),
                ('projects_link', models.URLField(blank=True, null=True)),
                ('resume', models.FileField(upload_to='')),
                ('noticePeriod', models.IntegerField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('full_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('employee_id', models.CharField(default=None, max_length=64, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=64)),
                ('temp_password', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.CharField(blank=True, max_length=100)),
                ('field2', models.CharField(default=100, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('requisition_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('job_description', models.FileField(upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('position_owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positionOwner', to='Incedoinc.employee')),
                ('raised_by_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raisedByEmployee', to='Incedoinc.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('pass', 'pass'), ('fail', 'fail'), ('pending', 'pending')], max_length=10)),
                ('rating_python', models.IntegerField(blank=True, null=True)),
                ('rating_java', models.IntegerField(blank=True, null=True)),
                ('rating_cpp', models.IntegerField(blank=True, null=True)),
                ('rating_sql', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, max_length=500, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('candidate_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.candidate')),
                ('interviewer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee')),
                ('requisition_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.job')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='registered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee'),
        ),
    ]
