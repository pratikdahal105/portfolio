import uuid
from django.db import models
from django.contrib.auth.models import User

class Socials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='socials')
    account_name = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='socials_logo/', blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_name}"

    class Meta:
        db_table = 'socials'