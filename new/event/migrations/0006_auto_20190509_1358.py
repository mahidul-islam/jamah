# Generated by Django 2.2 on 2019-05-09 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20190509_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionin',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Account'),
        ),
        migrations.AlterField(
            model_name='transactionout',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Account'),
        ),
    ]
