# Generated by Django 4.1.5 on 2023-03-07 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reciption', '0010_sortleave_late_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sortleave',
            name='entering_time',
        ),
        migrations.RemoveField(
            model_name='sortleave',
            name='late_entry',
        ),
        migrations.RemoveField(
            model_name='sortleave',
            name='leave_hour',
        ),
    ]
