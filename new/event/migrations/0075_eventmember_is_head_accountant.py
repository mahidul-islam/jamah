# Generated by Django 2.2.1 on 2019-06-06 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0074_auto_20190606_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='is_head_accountant',
            field=models.BooleanField(default=False),
        ),
    ]
