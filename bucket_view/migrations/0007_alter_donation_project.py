# Generated by Django 3.2.3 on 2021-09-08 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bucket_view', '0006_project_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bucket_view.project'),
        ),
    ]
