from django_filters import rest_framework as django_filters
from django_filters import rest_framework as filters
from account.models import Deposit, Withdrawal
from django.contrib.auth import get_user_model

User = get_user_model()

class DepositFilter(django_filters.FilterSet):  # Use django_filters for FilterSet
    date_min = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    status = django_filters.CharFilter(field_name="status", lookup_expr='iexact')  # Case insensitive

    class Meta:
        model = Deposit
        fields = ['code', 'status', 'date_min', 'date_max']

class WithdrawalFilter(django_filters.FilterSet):  # Use django_filters for FilterSet
    date_min = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    status = django_filters.CharFilter(field_name="status", lookup_expr='iexact')

    class Meta:
        model = Withdrawal
        fields = ['status', 'date_min', 'date_max']

class UserFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active")
    date_joined_min = filters.DateFilter(field_name="date_joined", lookup_expr='gte')
    date_joined_max = filters.DateFilter(field_name="date_joined", lookup_expr='lte')

    class Meta:
        model = User  # Ensure `model` is correctly pointing to the User model
        fields = ['is_active', 'date_joined_min', 'date_joined_max']