# Generated by Django 3.2.3 on 2023-02-03 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSlipFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.IntegerField()),
                ('action', models.TextField(null=True)),
            ],
        ),
    ]
