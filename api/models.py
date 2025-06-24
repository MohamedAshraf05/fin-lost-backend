from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Custom user model
class User(AbstractUser):
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def average_rating(self):
        ratings = self.received_ratings.all()
        return round(sum(r.rating for r in ratings) / len(ratings), 2) if ratings else None


# Item categories
class ItemType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Lost or Found Ad
class Ad(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location_description = models.TextField()
    exact_address = models.CharField(max_length=255, blank=True)
    transportation_type = models.CharField(max_length=255, blank=True, null=True) # How to deliver
    date_time = models.DateTimeField() # date found item
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False) # Item delivered successfully
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

# Chat model for conversation history
class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# Optional: Track user's ad or search history
class AdInteractionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=[('viewed', 'Viewed'), ('contacted', 'Contacted')])
    timestamp = models.DateTimeField(auto_now_add=True)

# User Rating
class UserRating(models.Model):
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_ratings')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rater', 'rated_user', 'ad')

    def __str__(self):
        return f"{self.rater} rated {self.rated_user}: {self.rating}/5"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.ad.is_resolved:
            raise ValidationError("Rating can only be submitted for resolved ads.")