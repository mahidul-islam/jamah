# Generated by Django 2.2.1 on 2019-06-02 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190602_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
