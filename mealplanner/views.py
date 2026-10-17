from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response

from mealplanner.serializers import UserSerializers,MealEntrySerializer
from mealplanner.models import MealEntry
from mealplanner.permissions import IsOwner

from datetime import datetime

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializers(data =form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializers(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class GetMeView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username = auth_user)

        serializer_instance= UserSerializers(instance)

        return Response(data=serializer_instance.data)

class MealEntryListCreate(APIView):

    authentication_classes =[ authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]
   
    def get(self,request):

        instance = MealEntry.objects.filter(owner= request.user)

        serializer_instance = MealEntrySerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data 

        serializer_instance = MealEntrySerializer(data= form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner = request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class MealEntryRetrieveUpdateDeleteView(APIView):

    #authentication_classes =[ authentication.BasicAuthentication]
    authentication_classes = [ authentication.TokenAuthentication]
    
    #permission_classes=[permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    

    def get(self,request,pk=None):

        instance = get_object_or_404(MealEntry,id=pk,owner=request.user)

        serializer_instance = MealEntrySerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance=get_object_or_404(MealEntry,id=pk)

        form_data= request.data

        serialier_instance = MealEntrySerializer(data=form_data,instance=instance)

        if serialier_instance.is_valid():

            serialier_instance.save()

            return Response(data= serialier_instance.data)

        else:

            return Response(data= serialier_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(MealEntry,id=pk)

        instance.delete()

        return Response(data={"message": "MealEntry deleted"})



class MealSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        response_data = {
            "todays_total": 0
        }

        current_date = datetime.now().date()

        current_month = datetime.now().month

        current_year = datetime.now().year

        # monthly summary
        current_month_transactions = MealEntry.objects.filter(
            owner=request.user,
            created_at__month=current_month,
            created_at__year=current_year
        )

        if current_month_transactions:

            monthly_total = current_month_transactions.values("calorie").aggregate(
                total=Sum("calorie")
            ).get("total")

            response_data["montly_total"] = monthly_total

        # total summary
        todays_transactions = MealEntry.objects.filter(
            owner=request.user,
            created_at__date=current_date
        )

        if todays_transactions.exists():

            todays_total = todays_transactions.aggregate(
                total=Sum("calorie")
            ).get("total")

            # total category summary
            category_summary = todays_transactions.values(
                "meal_type"
            ).annotate(total=Sum("calorie"))

            response_data["category_summary"] = category_summary

            response_data["todays_total"] = todays_total

        return Response(data=response_data)
