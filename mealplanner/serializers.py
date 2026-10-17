from django.contrib.auth.models import User
from rest_framework import serializers
from mealplanner.models import MealEntry

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model= User

        fields = ["username","email","password"]

        read_only_fields = ["id"]


class MealEntrySerializer(serializers.ModelSerializer):


    class Meta:

        model = MealEntry

        fields = "__all__"

        read_only_fields = ["id","owner","created_at","updated_at"]