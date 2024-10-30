from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from rest_framework.decorators import action


class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def validate_deposit(self, request, pk=None):
        """Validate a deposit if the user is an admin."""
        deposit = get_object_or_404(Deposit, pk=pk)

        if not deposit.is_validated:
            deposit.is_validated = True
            deposit.validated_by = request.user
            deposit.save()
            return Response({'status': 'Deposit validated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Already validated'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='user-deposits')
    def user_deposits(self, request):
        """Retrieve all deposits for the authenticated user."""
        user = request.user
        deposits = Deposit.objects.filter(user=user).order_by('-created_at')
        serializer = self.get_serializer(deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=['get'], url_path='user-withdrawals')
    def user_withdrawals(self, request):
        """Retrieve all withdrawals for the authenticated user."""
        user = request.user
        withdrawals = Withdrawal.objects.filter(user=user).order_by('-created_at')
        serializer = self.get_serializer(withdrawals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def validate_withdrawal(self, request, pk=None):
        """Validate a withdrawal if the user is an admin."""
        withdrawal = get_object_or_404(Withdrawal, pk=pk)

        if not withdrawal.is_validated:
            withdrawal.is_validated = True
            withdrawal.validated_by = request.user
            withdrawal.save()
            return Response({'status': 'Withdrawal validated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Already validated'}, status=status.HTTP_400_BAD_REQUEST)
