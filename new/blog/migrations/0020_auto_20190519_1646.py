# Generated by Django 2.2.1 on 2019-05-19 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20190519_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteforblog',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
    ]
