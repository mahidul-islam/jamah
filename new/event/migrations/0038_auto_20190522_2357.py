# Generated by Django 2.2.1 on 2019-05-22 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0037_auto_20190522_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='needed_approve',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='transactionin',
            name='part_of_cost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_transaction_ins', to='event.Cost'),
        ),
    ]