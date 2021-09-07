# Generated by Django 3.2.3 on 2021-08-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bucket_view', '0003_alter_project_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='adult',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donation',
            name='consent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donation',
            name='data',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='propertyId',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]