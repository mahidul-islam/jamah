# Generated by Django 2.2.1 on 2019-06-02 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0064_auto_20190602_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cost_account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
