from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, WithdrawalViewSet

router = DefaultRouter()
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'withdrawals', WithdrawalViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
    path('deposits/<uuid:pk>/validate/', DepositViewSet.as_view({'post': 'validate_deposit'}), name='validate-deposit'),
    path('withdrawals/<uuid:pk>/validate/', WithdrawalViewSet.as_view({'post': 'validate_withdrawal'}), name='validate-withdrawal'),
]
