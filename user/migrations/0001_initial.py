# Generated by Django 5.1.4 on 2024-12-18 05:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=100)),
                ('business_description', models.TextField(blank=True)),
                ('seller_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_sales', models.IntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.TextField(blank=True)),
                ('preferred_payment_method', models.CharField(blank=True, max_length=50)),
                ('purchase_history_count', models.IntegerField(default=0)),
                ('buyer_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]
