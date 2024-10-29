from rest_framework import serializers
from .models import Deposit, Withdrawal

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'code', 'amount', 'date', 'status', 'is_validated', 'validated_by', 'user']


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'amount', 'date', 'is_validated', 'validated_by', 'user']
