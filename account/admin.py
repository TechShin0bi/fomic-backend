from django.contrib import admin
from .models import Deposit, Withdrawal

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', 'status', 'is_validated', 'validated_by', 'user', 'date']
    list_filter = ['status', 'is_validated', 'validated_by']
    actions = ['validate_deposit']

    def validate_deposit(self, request, queryset):
        queryset.update(is_validated=True, validated_by=request.user)
        self.message_user(request, "Selected deposits have been validated.")

    validate_deposit.short_description = "Validate selected deposits"


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['amount', 'is_validated', 'validated_by', 'user', 'date']
    list_filter = ['is_validated', 'validated_by']
    actions = ['validate_withdrawal']

    def validate_withdrawal(self, request, queryset):
        queryset.update(is_validated=True, validated_by=request.user)
        self.message_user(request, "Selected withdrawals have been validated.")

    validate_withdrawal.short_description = "Validate selected withdrawals"
