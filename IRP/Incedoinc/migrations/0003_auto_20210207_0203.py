# Generated by Django 3.1.5 on 2021-02-06 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Incedoinc', '0002_auto_20210207_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
    ]
