# Generated by Django 2.2.1 on 2019-05-24 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0058_event_event_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
