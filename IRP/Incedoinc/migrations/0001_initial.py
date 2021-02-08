# Generated by Django 3.1.5 on 2021-02-08 13:35

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
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('college_name', models.CharField(blank=True, max_length=254, null=True)),
                ('CGPA', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('experience', models.IntegerField()),
                ('mobile', models.CharField(max_length=10)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('projects_link', models.URLField(blank=True, null=True)),
                ('resume', models.FileField(upload_to='Resume/')),
                ('notice_period', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('full_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('employee_id', models.CharField(default=None, max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('pass', 'pass'), ('fail', 'fail'), ('pending', 'pending')], max_length=10)),
                ('comments', models.TextField(blank=True, max_length=500, null=True)),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('candidate_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.candidate')),
                ('interviewer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee')),
            ],
        ),
        migrations.CreateModel(
            name='JD',
            fields=[
                ('jd_name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('jd_file', models.FileField(upload_to='JD/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee')),
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
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('jd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.jd')),
                ('position_owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_owner', to='Incedoinc.employee')),
                ('raised_by_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raised_by_employee', to='Incedoinc.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('field_id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=20)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, max_length=100, null=True)),
                ('feedback_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.feedback')),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='requisition_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.job'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='registered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee'),
        ),
    ]
