# Generated by Django 3.2.3 on 2021-09-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bucket_view', '0004_auto_20210826_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='researcher_affiliation',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='researcher_name',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
