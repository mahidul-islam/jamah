# Generated by Django 2.2.1 on 2019-05-23 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0044_cost_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='name',
            field=models.CharField(default='name', max_length=255),
        ),
    ]
