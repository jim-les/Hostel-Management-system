# Generated by Django 5.0.6 on 2024-06-27 14:35

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10)),
                ('rent_amount', models.DecimalField(decimal_places=2, default=4000.0, max_digits=10)),
                ('has_food', models.BooleanField(default=False)),
                ('arrears', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('adm_date', models.DateField(null=True)),
                ('number', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('month_paid', models.CharField(max_length=100)),
                ('mpesa_ref', models.CharField(max_length=15)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('reciept', models.CharField(max_length=15, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenants.student')),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('response_text', models.TextField(blank=True, null=True)),
                ('responded', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenants.student')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenants.student')),
            ],
        ),
        migrations.CreateModel(
            name='MealTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenants.student')),
            ],
        ),
        migrations.CreateModel(
            name='MealRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], max_length=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('served', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenants.student')),
            ],
            options={
                'unique_together': {('student', 'meal', 'date')},
            },
        ),
    ]
