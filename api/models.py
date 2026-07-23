from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserPreferences(models.Model):
    """
    Individual settings to adapt API responses 
    and user alert behavior.
    """
    UNIT_CHOICES = [
        ('C', 'Celsius'),
        ('F', 'Fahrenheit'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('none', 'Disabled'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    temperature_unit = models.CharField(max_length=1, choices=UNIT_CHOICES, default='C')
    email_notifications = models.BooleanField(default=True)
    summary_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily', help_text="Frequency of the periodic report (daily, weekly, or disabled)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self):
        return f"Preferences for {self.user.username}"

# Signals for automatic creation of User Preferences
@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Automatically creates default preferences 
    when a new user registers.
    """
    if created:
        UserPreferences.objects.create(user=instance)




