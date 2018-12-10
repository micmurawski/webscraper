# Generated by Django 2.1.2 on 2018-12-07 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20181206_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='target_url',
            field=models.URLField(max_length=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('0', 'MAIN'), ('1', 'SUB_TASK')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='visitedtarget',
            name='target_url',
            field=models.URLField(max_length=255),
        ),
    ]