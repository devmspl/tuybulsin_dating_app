# Generated by Django 3.2.25 on 2024-03-13 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium')], default='basic', max_length=20)),
                ('features1', models.TextField()),
                ('features2', models.TextField()),
                ('features3', models.TextField()),
            ],
        ),
    ]
