from django.urls import path

from mealplanner.views import SignUpView,GetMeView
from mealplanner.views import MealEntryListCreate,MealEntryRetrieveUpdateDeleteView
from mealplanner.views import MealSummaryView

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns=[

    path('signup/',SignUpView.as_view()),
    path('me/',GetMeView.as_view()),
    path('meal-entries/',MealEntryListCreate.as_view()),
    path('meal-entries/<int:pk>/',MealEntryRetrieveUpdateDeleteView.as_view()),
    path("meals/summary/", MealSummaryView.as_view()),

    path("login/", obtain_auth_token),
]