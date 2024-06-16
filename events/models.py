from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    reminder = models.BooleanField(default=False)
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True)

    def __str__(self):
        return F"{self.title} - {self.date} - {self.location}"



class ExternalUser(models.Model):
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name='external_users', blank=True)

    def __str__(self):
        return F"{self.email} - {self.events.count()} events"
