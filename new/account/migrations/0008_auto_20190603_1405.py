# Generated by Django 2.2.1 on 2019-06-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_account_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='description',
            field=models.CharField(max_length=100),
        ),
    ]
