# Generated by Django 3.2.7 on 2021-10-14 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='disccount',
        ),
    ]
