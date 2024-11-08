from django.urls import path
from .views import *

urlpatterns = [
    path('plans/', PlanListCreateView.as_view(), name='plan-list-create'),
    path('user_plans/', UpdateUserPlanView.as_view(), name='plan-user_plans'),
    path('create-plans/', CreatePlansView.as_view(), name='create-plans'),
]
