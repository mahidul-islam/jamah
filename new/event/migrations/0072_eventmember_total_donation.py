# Generated by Django 2.2.1 on 2019-06-05 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0071_auto_20190604_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='total_donation',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]