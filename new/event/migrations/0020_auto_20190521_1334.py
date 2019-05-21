# Generated by Django 2.2.1 on 2019-05-21 13:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0019_auto_20190519_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionin',
            name='is_donation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='official_blog',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
        migrations.AlterField(
            model_name='transactionin',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Account'),
        ),
        migrations.AlterField(
            model_name='transactionin',
            name='comes_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.EventMember'),
        ),
        migrations.AlterField(
            model_name='transactionout',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Account'),
        ),
        migrations.AlterField(
            model_name='transactionout',
            name='goes_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.EventMember'),
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('per_head_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.EventMember')),
            ],
        ),
        migrations.AddField(
            model_name='transactionin',
            name='part_of_cost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='event.Cost'),
        ),
    ]