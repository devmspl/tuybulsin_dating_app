# Generated by Django 3.2.25 on 2024-03-18 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalprofile', '0006_auto_20240318_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='year_of_birth',
            field=models.CharField(default=0, max_length=50),
        ),
    ]