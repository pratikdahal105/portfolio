# Generated by Django 4.2.7 on 2024-03-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='skills_used',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
