import uuid
from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill_name}"

    class Meta:
        db_table = 'skills'