# Generated by Django 2.2.1 on 2019-05-28 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_mother_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='comes_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_outs', to='account.Account'),
        ),
    ]
