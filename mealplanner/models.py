from django.db import models

from django.contrib.auth.models import User

class FoodLog(models.Model):

    title = models.CharField(max_length=200)

    calorie = models.PositiveIntegerField()

    MEAL_TYPE_CHOICES = (
        ("BREAKFAST","breakfast"),
        ("LUNCH","lunch"),
        ("DINNER","dinner"),
        ("SNACKS","snacks")
    )

    meal_type = models.CharField(max_length=200,choices=MEAL_TYPE_CHOICES,default="LUNCH")

    serving_size = models.CharField(max_length=200)

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)