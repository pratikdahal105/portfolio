import uuid
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact')
    mail_from = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    subject = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.award_name}"

    class Meta:
        db_table = 'contact'
