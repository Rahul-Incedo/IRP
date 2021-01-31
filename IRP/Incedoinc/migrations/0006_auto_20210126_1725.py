# Generated by Django 3.1.5 on 2021-01-26 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Incedoinc', '0005_auto_20210126_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='requisitionId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.job'),
        ),
        migrations.AddField(
            model_name='candidatejobinfo',
            name='level1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='level1', to='Incedoinc.feedback'),
        ),
        migrations.AddField(
            model_name='candidatejobinfo',
            name='level2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='level2', to='Incedoinc.feedback'),
        ),
        migrations.AddField(
            model_name='candidatejobinfo',
            name='level3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='level3', to='Incedoinc.feedback'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='registeredBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.employee'),
        ),
    ]
