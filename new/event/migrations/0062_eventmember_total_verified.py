# Generated by Django 2.2.1 on 2019-05-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0061_auto_20190528_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='total_verified',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
