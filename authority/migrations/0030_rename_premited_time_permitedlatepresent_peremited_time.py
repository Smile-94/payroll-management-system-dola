# Generated by Django 4.1.5 on 2023-03-02 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0029_alter_permitedlatepresent_salary_diduction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permitedlatepresent',
            old_name='premited_time',
            new_name='peremited_time',
        ),
    ]