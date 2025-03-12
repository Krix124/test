from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class EventRegistration(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_proof = models.ImageField(upload_to='payment_proofs/')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    current_participants = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    registered_users = models.ManyToManyField(User, through=EventRegistration)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']

    @property
    def is_full(self):
        return self.current_participants >= self.max_participants
