# Generated by Django 2.2 on 2019-05-09 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20190509_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Boss', to=settings.AUTH_USER_MODEL),
        ),
    ]
