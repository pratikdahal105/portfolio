import uuid
from django.db import models
from django.contrib.auth.models import User

class Award(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    award_date = models.DateField(blank=True, null=True)
    awarded_by = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.award_name}"

    class Meta:
        db_table = 'awards'
