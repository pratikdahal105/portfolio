from django.db import models
from django.contrib.auth.models import User

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField(max_length=200, blank=True)
    school_location = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='education_images/', blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.degree} - {self.school_name}"

    class Meta:
        db_table = 'education'