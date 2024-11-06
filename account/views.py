from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework import generics, filters as rest_filters
from django_filters import rest_framework as filters
from common.filters import DepositFilter , WithdrawalFilter
from common.paginations import StandardResultsPagination

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
        user = request.user

        # Check if the requested withdrawal amount is available in the user's balance
        amount = data.get('amount')
        if amount is None:
            return Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for sufficient balance
        if user.balance < amount:
            return Response({"error": "Insufficient balance to create this withdrawal."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with withdrawal creation if balance is sufficient
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        withdrawal = serializer.save()

        # Deduct the amount from the user's balance
        user.balance -= amount
        user.save()

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



class ValidateDepositView(UpdateAPIView):
    """
    View to validate a deposit.
    Only admins or staff members are allowed to validate deposits.
    """
    permission_classes = [IsAuthenticated]
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    
    def put(self, request, pk, *args, **kwargs):
        # Check if the user is an admin or staff member
        if not request.user.is_admin:
            return Response({"error": "You do not have permission to validate deposits."}, status=status.HTTP_403_FORBIDDEN)

        # Get the deposit object or return a 404 if not found
        deposit = get_object_or_404(Deposit, pk=pk)

        # Check if deposit is already validated
        if deposit.is_validated:
            return Response({"error": "This deposit has already been validated."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the deposit
        deposit.is_validated = True
        deposit.validated_by = request.user
        deposit.status = 'completed'
        user = deposit.user
        user.balance += deposit.amount
        user.save()
        deposit.save()

        return Response(DepositSerializer(deposit).data)


class ValidateWithdrawalView(UpdateAPIView):
    """
    View to validate a withdrawal.
    Only admins or staff members are allowed to validate withdrawals.
    """
    permission_classes = [IsAuthenticated]
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer

    def put(self, request, pk, *args, **kwargs):
        # Check if the user is an admin or staff member
        if not request.user.is_admin:
            return Response({"error": "You do not have permission to validate withdrawals."}, status=status.HTTP_403_FORBIDDEN)

        # Get the withdrawal object or return a 404 if not found
        withdrawal = get_object_or_404(Withdrawal, pk=pk)

        # Check if withdrawal is already validated
        if withdrawal.is_validated:
            return Response({"error": "This withdrawal has already been validated."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user has enough balance
        user = withdrawal.user
        if user.balance < withdrawal.amount:
            return Response({"error": "Insufficient balance to complete this withdrawal."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the withdrawal
        withdrawal.is_validated = True
        withdrawal.validated_by = request.user
        withdrawal.status = 'completed'

        # Deduct the amount from user's balance
        user.balance -= withdrawal.amount
        user.save()
        withdrawal.save()

        return Response(WithdrawalSerializer(withdrawal).data)
    
    
class DepositListView(generics.ListAPIView):
    queryset = Deposit.objects.all().order_by('-created_at')
    serializer_class = DepositSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_class = DepositFilter
    search_fields = ['code']  # Search by deposit code

class WithdrawalListView(generics.ListAPIView):
    queryset = Withdrawal.objects.all().order_by('-created_at')
    serializer_class = WithdrawalSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_class = WithdrawalFilter
    search_fields = ['withdrawalCode']  # Search by withdrawal code