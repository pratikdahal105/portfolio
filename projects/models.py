import uuid
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    repo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.project_name}"

    class Meta:
        db_table = 'project'