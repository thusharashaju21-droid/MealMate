from django.db import models
from django.contrib.auth.models import User

class MealEntry(models.Model):

    title = models.CharField(max_length=200)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_entries')

    calorie = models.PositiveIntegerField()

    MEAL_CHOICES = [
            ("BREAKFAST", "Breakfast"),
            ("LUNCH", "Lunch"),
            ("DINNER", "Dinner"),
            ("SNACKS", "Snacks"),
        ]

    meal_type = models.CharField(max_length=60,choices=MEAL_CHOICES)

    serving_size = models.CharField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        
        return self.title

    