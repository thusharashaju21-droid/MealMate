
from rest_framework import serializers

from django.contrib.auth.models import User

from mealplanner.models import FoodLog

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id","username","email","password"]

        read_only_fields = ["id"]

class FoodLogSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = FoodLog

        fields = "__all__"

        read_only_fields = ["id","owner","created_at"]