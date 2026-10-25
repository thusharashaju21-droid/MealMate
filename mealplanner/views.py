from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from datetime import datetime

from mealplanner.serializers import SignUpSerializer,FoodLogSerializer
from mealplanner.models import FoodLog
from mealplanner.permissions import IsOwner
from mealplanner.ai_service import get_diet_plan

class RegisterView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = SignUpSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = SignUpSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class GetMeView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username = auth_user)

        serializer_instance = SignUpSerializer(instance)

        return Response(data=serializer_instance.data)

class FoodLogListCreateView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        instance = FoodLog.objects.filter(owner=request.user)

        serializer_instance = FoodLogSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = FoodLogSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class FoodLogRetrieveUpdateDeleteView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = FoodLogSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data= serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})

class FoodLogSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {
            "todays_total_calorie":0
        }

        cur_date = datetime.now().date()
        cur_month = datetime.now().month
        cur_year = datetime.now().year

        # todays total calorie

        todays_foodlog = FoodLog.objects.filter(owner=request.user,created_at__date=cur_date)

        if todays_foodlog:

            today_total_cal = todays_foodlog.values("calorie").aggregate(total=Sum("calorie")).get("total")
            today_cat_total_cal = todays_foodlog.values("meal_type").annotate(total=Sum("calorie"))

            response_data["todays_total_calorie"] = today_total_cal
            response_data["todays_category_total_calorie"] = today_cat_total_cal

        # monthly total calorie

        monthly_foodlog = FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_foodlog:

            monthly_total_cal = monthly_foodlog.values("calorie").aggregate(total=Sum("calorie")).get("total")
            monthly_cat_total_cal = monthly_foodlog.values("meal_type").annotate(total=Sum("calorie"))

            response_data["monthly_total_calorie"] = monthly_total_cal
            response_data["monthly_category_total_calorie"] = monthly_cat_total_cal

        return Response(data=response_data)

class DietPlanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data = {"monthly_total_calorie":0}

        cur_month = datetime.now().month
        cur_year = datetime.now().year

        monthly_calorie = FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_calorie:

            monthly_total_calorie = monthly_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")
            category_total_calorie = monthly_calorie.values("meal_type").annotate(total=Sum("calorie"))

            response_data["monthly_total_calorie"] = monthly_total_calorie
            response_data["category_total_calorie"] = category_total_calorie

            diet_plan = get_diet_plan(response_data)
            response_data["Diet Plan"] = diet_plan

        return Response(data=response_data)