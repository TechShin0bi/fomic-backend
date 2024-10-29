from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Assign the deposit to the authenticated user."""
        serializer.save(user=self.request.user)

    def validate_deposit(self, request, pk=None):
        """Validate a deposit if the user is an admin."""
        deposit = get_object_or_404(Deposit, pk=pk)

        if not deposit.is_validated:
            deposit.is_validated = True
            deposit.validated_by = request.user
            deposit.save()
            return Response({'status': 'Deposit validated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Already validated'}, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Assign the withdrawal to the authenticated user."""
        serializer.save(user=self.request.user)

    def validate_withdrawal(self, request, pk=None):
        """Validate a withdrawal if the user is an admin."""
        withdrawal = get_object_or_404(Withdrawal, pk=pk)

        if not withdrawal.is_validated:
            withdrawal.is_validated = True
            withdrawal.validated_by = request.user
            withdrawal.save()
            return Response({'status': 'Withdrawal validated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Already validated'}, status=status.HTTP_400_BAD_REQUEST)
