# Generated by Django 2.2.1 on 2019-05-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0056_auto_20190524_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='per_head_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]