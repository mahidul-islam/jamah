# Generated by Django 2.2.1 on 2019-05-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamah', '0013_auto_20190524_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='jamahmember',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
    ]