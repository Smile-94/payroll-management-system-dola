# Generated by Django 4.1.5 on 2023-02-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0017_monthlyoffday_monthlyholiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyholiday',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='monthlyoffday',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
