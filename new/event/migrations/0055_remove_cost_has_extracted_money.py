# Generated by Django 2.2.1 on 2019-05-24 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0054_eventmember_is_accountant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='has_extracted_money',
        ),
    ]
