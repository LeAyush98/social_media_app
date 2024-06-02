from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.CharField(max_length=50)
    to_user = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default = "Pending")  # Pending, Accepted, Rejected
    creation_time = models.DateTimeField(auto_now_add=True)

