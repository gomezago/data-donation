# Generated by Django 3.2.3 on 2023-06-07 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bucket_view', '0014_auto_20230605_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menstruation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle', models.BooleanField(default=False)),
                ('last_date', models.DateField()),
                ('usual', models.CharField(default=None, max_length=200, null=True)),
                ('suffer', models.CharField(default=None, max_length=200, null=True)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bucket_view.donation')),
            ],
        ),
        migrations.CreateModel(
            name='Curation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(default=None, max_length=1, null=True)),
                ('sleep', models.CharField(default=None, max_length=1, null=True)),
                ('hr', models.CharField(default=None, max_length=1, null=True)),
                ('time', models.CharField(default=None, max_length=1, null=True)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bucket_view.donation')),
            ],
        ),
    ]
