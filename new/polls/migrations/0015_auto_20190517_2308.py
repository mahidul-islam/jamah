# Generated by Django 2.2.1 on 2019-05-17 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20190517_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.Choice'),
        ),
    ]