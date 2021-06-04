# Generated by Django 3.2.3 on 2021-06-04 15:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bucket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bucketuser',
            name='id',
            field=models.CharField(max_length=100),
        ),
    ]
