# Generated by Django 2.2.1 on 2019-05-19 18:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_auto_20190519_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
