# Generated by Django 3.0.5 on 2020-04-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(choices=[('IT', 'IT'), ('ECE', 'ECE'), ('CS', 'CS'), ('ME', 'ME')], max_length=100),
        ),
    ]
