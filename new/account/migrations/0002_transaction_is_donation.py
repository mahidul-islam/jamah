# Generated by Django 2.2.1 on 2019-05-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_donation',
            field=models.BooleanField(default=False),
        ),
    ]