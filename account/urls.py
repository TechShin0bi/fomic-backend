from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'withdrawals', WithdrawalViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
    path('deposits/<uuid:pk>/validate/', DepositViewSet.as_view({'post': 'validate_deposit'}), name='validate-deposit'),
    path('withdrawals/<uuid:pk>/validate/', WithdrawalViewSet.as_view({'post': 'validate_withdrawal'}), name='validate-withdrawal'),
    
    path('validate-deposit/<uuid:pk>/', ValidateDepositView.as_view(), name='validate-deposit'),
    path('validate-withdrawal/<uuid:pk>/', ValidateWithdrawalView.as_view(), name='validate-withdrawal'),

    path('deposits-list/', DepositListView.as_view(), name='deposit-list'),
    path('withdrawal-list/', WithdrawalListView.as_view(), name='withdrawal-list'),
]
