# Generated by Django 2.2.1 on 2019-05-21 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0022_auto_20190521_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='official_blog',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
    ]
