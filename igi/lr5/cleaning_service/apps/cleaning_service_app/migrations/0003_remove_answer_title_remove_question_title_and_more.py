# Generated by Django 5.0.6 on 2024-05-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_service_app', '0002_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telephone',
            field=models.CharField(default='+375290000000', max_length=13, null=True),
        ),
    ]
