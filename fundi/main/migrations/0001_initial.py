# Generated by Django 5.0.1 on 2024-02-14 09:59

import django.db.models.deletion
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.PositiveIntegerField()),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('license_plate_number', models.CharField(help_text="Enter a license plate number starting with 'T' followed by three digits, and three letters.", max_length=7, unique=True, validators=[main.models.validate_license_plate_number])),
                ('mileage', models.PositiveIntegerField(default=0)),
                ('fuel_type', models.CharField(choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')], max_length=20)),
                ('transmission_type', models.CharField(choices=[('manual', 'Manual Transmission'), ('automatic', 'Automatic Transmission')], max_length=20)),
                ('next_service_due', models.DateField(blank=True, null=True)),
                ('last_service_date', models.DateField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.carowner')),
            ],
        ),
        migrations.CreateModel(
            name='RepairRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_model', models.CharField(max_length=255)),
                ('license_plate', models.CharField(max_length=20)),
                ('issue_description', models.TextField()),
                ('additional_comments', models.TextField()),
                ('repair_type', models.CharField(max_length=255)),
                ('preferred_date', models.DateField()),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('owner_latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('owner_longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.car')),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('availability', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepairAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_time', models.DateTimeField(auto_now_add=True)),
                ('completion_time', models.DateTimeField(blank=True, null=True)),
                ('repair_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.repairrequest')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.technician')),
            ],
        ),
        migrations.CreateModel(
            name='TechnicianAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_time', models.DateTimeField()),
                ('technician_latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('technician_longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.technician')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('owner', 'Car Owner'), ('technician', 'Technician')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
