
from django.urls import path

from mealplanner.views import RegisterView,GetMeView,FoodLogListCreateView,FoodLogRetrieveUpdateDeleteView,FoodLogSummaryView,DietPlanView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    #  register view
    path("register/",RegisterView.as_view()),

    #  getme view
    path("me/",GetMeView.as_view()),

    # foodlog list,create view
    path("foodlog/",FoodLogListCreateView.as_view()),

    # foodlog retrieve,update,delete view
    path("foodlog/<int:pk>/",FoodLogRetrieveUpdateDeleteView.as_view()),

    # token authentication
    path("token/",ObtainAuthToken.as_view()),

    # summary view
    path("foodlog/summary/",FoodLogSummaryView.as_view()),

    # dietplan view
    path("foodlog/diet/",DietPlanView.as_view()),
]