from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

User = settings.AUTH_USER_MODEL

def future_date_validator(value):
    if value < timezone.now():
        raise ValueError("Event date must be in the future.")

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)

class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events')
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(max_length=2000)
    location = models.CharField(max_length=140)
    starts_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['starts_at']
        permissions = [
            ("approve_event", "Can approve event"),
        ]

    def __str__(self):
        return f"{self.title} @ {self.starts_at:%Y-%m-%d}"

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    @property
    def tickets_count(self):
        return self.tickets.count()

    def save(self, *args, **kwargs):
        if self.starts_at < timezone.now():
            raise ValueError("Event date must be in the future.")
        if not self.slug:
            base = slugify(self.title)[:130]
            maybe = base
            i = 1
            while Event.objects.filter(slug=maybe).exclude(pk=self.pk).exists():
                i += 1
                maybe = f"{base}-{i}"
            self.slug = maybe
        super().save(*args, **kwargs)

class Ticket(models.Model):
    class Seat(models.TextChoices):
        STANDARD = 'standard', 'Standard'
        VIP = 'vip', 'VIP'
        PREMIUM = 'premium', 'Premium'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    seat_type = models.CharField(max_length=20, choices=Seat.choices, default=Seat.STANDARD)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # one ticket per user per event
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.seat_type})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event} by {self.user} ({self.rating}/5)"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} ❤️ {self.event}"
