# Generated by Django 3.2.25 on 2024-03-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalprofile', '0007_auto_20240318_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
