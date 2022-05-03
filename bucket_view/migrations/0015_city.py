# Generated by Django 3.2.3 on 2022-05-03 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bucket_view', '0014_auto_20220502_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default=None, max_length=50, null=True)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bucket_view.donation')),
            ],
        ),
    ]