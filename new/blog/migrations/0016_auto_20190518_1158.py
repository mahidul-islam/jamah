# Generated by Django 2.2.1 on 2019-05-18 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20190518_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteforblog',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
    ]
