# Generated by Django 3.1.6 on 2021-02-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0005_auto_20210225_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='data_info',
            field=models.TextField(null=True),
        ),
    ]