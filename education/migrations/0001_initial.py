# Generated by Django 4.2.7 on 2023-12-17 23:45

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
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=200)),
                ('school_location', models.CharField(blank=True, max_length=200)),
                ('degree', models.CharField(blank=True, max_length=100)),
                ('major', models.CharField(blank=True, max_length=100)),
                ('gpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='education_images/')),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
