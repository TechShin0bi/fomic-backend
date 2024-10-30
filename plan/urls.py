from django.urls import path
from .views import (
    PlanListCreateView,
    UserPlanListCreateView,
    UpdateUserPlanView,
    CreatePlansView,
    UserActivePlanView
)

urlpatterns = [
    path('plans/', PlanListCreateView.as_view(), name='plan-list-create'),
    path('user-plans/', UserPlanListCreateView.as_view(), name='user-plan-list-create'),
    path('user-active-plans/', UserActivePlanView.as_view(), name='user-plan-active'),
    path('update-plan/<uuid:user_id>/', UpdateUserPlanView.as_view(), name='update-user-plan'),
    path('create-plans/', CreatePlansView.as_view(), name='create-plans'),
]
