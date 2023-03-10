# Generated by Django 4.1.5 on 2023-03-02 08:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0030_rename_premited_time_permitedlatepresent_peremited_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermitedSortLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peremited_time', models.DurationField()),
                ('permited_days', models.PositiveIntegerField()),
                ('salary_diduction', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
