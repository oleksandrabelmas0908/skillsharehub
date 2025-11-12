
from django.db import models
from datetime import datetime


class Chanel(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    created_at = models.DateTimeField(default=datetime.now())

    owner = models.ForeignKey('mainapp.CustomUser', related_name="chanel_owner", on_delete=models.CASCADE)
    subscribers = models.ManyToManyField('mainapp.CustomUser', related_name="subscriber_list", blank=True)
    publications = models.ManyToManyField('mainapp.Post', related_name="chanel_posts", blank=True)

    def __str__(self):
        return self.name
    
    @property
    def subscriber_count(self):
        return self.subscribers.count()

    