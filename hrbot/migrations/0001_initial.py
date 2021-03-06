# Generated by Django 2.0 on 2018-03-23 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('emp_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=200)),
                ('last_name', models.CharField(blank=True, default='', max_length=200)),
                ('full_name', models.CharField(blank=True, default='', max_length=200)),
                ('designation', models.CharField(blank=True, default='', max_length=200)),
                ('mobile_no', models.IntegerField(default=0)),
                ('email_id', models.EmailField(default='', max_length=254)),
                ('joining_date', models.DateField()),
                ('creation_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('emp_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=200)),
                ('last_name', models.CharField(blank=True, default='', max_length=200)),
                ('designation', models.CharField(blank=True, default='', max_length=200)),
                ('mobile_no', models.IntegerField(default=0)),
                ('email_id', models.EmailField(default='', max_length=254)),
                ('joining_date', models.DateField()),
                ('creation_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('emp_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('total_leaves', models.IntegerField(default=6)),
                ('applied_leaves', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('yet_to_accrue', models.IntegerField(default=18)),
                ('creation_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('emp_tbl_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrbot.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('leave_type', models.CharField(default='paid time off', max_length=100)),
                ('duration', models.IntegerField(default=0)),
                ('leave_status', models.CharField(default='pending', max_length=100)),
                ('creation_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('emp_tbl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrbot.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DEFAULT', 'Default'), ('INCIDENT', 'Incident'), ('PROBLEM', 'Problem'), ('Request for Change', 'Request For Change')], max_length=30)),
                ('to', models.CharField(choices=[('IT', 'IT support'), ('HR', 'HR support'), ('FACILITY', 'Facility support'), ('APP', 'App support'), ('FINANCE', 'Finance support')], max_length=30)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('NORMAL', 'Normal'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('VERY HIGH', 'Very High')], max_length=30)),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hrbot.Employee')),
            ],
        ),
    ]
