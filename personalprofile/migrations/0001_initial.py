# Generated by Django 3.2.25 on 2024-03-08 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('year_of_birth', models.CharField(max_length=4)),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('W', 'Widowed'), ('O', 'Other')], max_length=1)),
                ('nationality', models.CharField(max_length=255)),
                ('height', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('education', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('residency_status', models.CharField(choices=[('RD', 'Residency Permit'), ('RR', 'Residency Rule'), ('R', 'Resident'), ('O', 'Other')], max_length=2)),
                ('religion', models.CharField(max_length=255)),
                ('religiousness_scale', models.IntegerField()),
                ('native_language', models.CharField(max_length=255)),
                ('other_languages', models.CharField(max_length=255)),
                ('other_skills', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('personal_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='personalprofile.personalinformation')),
            ],
        ),
    ]