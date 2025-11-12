from django.db import models
from datetime import datetime

from .user import CustomUser


class Chanel(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    created_at = models.DateTimeField(default=datetime.now())

    owner = models.ForeignKey(CustomUser, related_name="chanel_owner", on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(CustomUser, related_name="subscriber_list", blank=True)

    def __str__(self):
        return self.name
    
    @property
    def subscriber_count(self):
        return self.subscribers.count()

    