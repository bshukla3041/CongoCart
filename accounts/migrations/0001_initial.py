# Generated by Django 3.0.6 on 2020-05-23 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gst_field.modelfields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CongoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CongoUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('is_verified', models.BooleanField(default=False)),
                ('business_name', models.CharField(max_length=50)),
                ('gst_number', gst_field.modelfields.GSTField(max_length=15)),
                ('business_type', models.CharField(choices=[('R', 'Retailer'), ('W', 'Wholesaler')], default='R', max_length=1)),
                ('business_category', models.CharField(choices=[('EC', 'Electronics'), ('AP', 'Appliances'), ('FS', 'Fashion'), ('HD', 'Home Decoration'), ('GC', 'Groceries'), ('OT', 'Others')], max_length=2)),
                ('congo_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
