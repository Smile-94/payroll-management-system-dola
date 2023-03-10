# Generated by Django 4.1.5 on 2023-02-24 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0016_alter_leaveapplication_is_active'),
        ('employee', '0008_alter_employeesalary_basic_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlySalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_conveyance', models.FloatField()),
                ('total_food_allowance', models.FloatField()),
                ('total_medical_allowance', models.FloatField()),
                ('total_house_rent', models.FloatField()),
                ('total_mobile_allowance', models.FloatField()),
                ('late_present_diduct', models.FloatField(default=0.0)),
                ('sort_leave_diduct', models.FloatField(default=0.0)),
                ('extra_leave_diduct', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('festival_bonus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festival_bonus', to='authority.festivalbonus')),
                ('salary_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_employee', to='employee.employeeinfo')),
                ('salary_month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_month', to='authority.payrollmonth')),
            ],
        ),
    ]
