# Generated by Django 2.2.1 on 2019-05-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0045_auto_20190523_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]