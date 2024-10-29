from django.urls import path
from .views import PlanListCreateView, PlanDetailView,UserPlanListCreateView, UserPlanDetailView,UpdateUserPlanView

urlpatterns = [
    path('plans/', PlanListCreateView.as_view(), name='plan-list-create'),
    path('plans/<uuid:pk>/', PlanDetailView.as_view(), name='plan-detail'),
    path('user-plans/', UserPlanListCreateView.as_view(), name='user-plan-list-create'),
    path('user-plans/<uuid:pk>/', UserPlanDetailView.as_view(), name='user-plan-detail'),
    path('update-plan/<int:user_id>/', UpdateUserPlanView.as_view(), name='update-user-plan'),
]
