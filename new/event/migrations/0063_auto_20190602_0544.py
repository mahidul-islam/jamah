# Generated by Django 2.2.1 on 2019-06-02 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0062_eventmember_total_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='total_sent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='eventmember',
            name='account',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]