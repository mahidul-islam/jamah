# Generated by Django 2.2 on 2019-05-09 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20190509_1214'),
        ('polls', '0007_voter_choice_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.Event'),
        ),
    ]
