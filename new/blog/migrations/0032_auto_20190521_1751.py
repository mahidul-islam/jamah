# Generated by Django 2.2.1 on 2019-05-21 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20190521_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteforblog',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
    ]
