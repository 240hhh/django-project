from django.urls import path
from . import views

app_name = "duty_management"
urlpatterns = [
    path('',views.index, name="index"),
    path('reserve/',views.reserve, name="reserve"),
    path('reserve/decision',views.reserve_decision, name="reserve_decision")
]