# Generated by Django 2.2.1 on 2019-06-04 06:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0069_auto_20190604_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]