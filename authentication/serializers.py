from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class GetUserSerializer(serializers.ModelSerializer):
    from account.serializers import DepositSerializer , WithdrawalSerializer
    from plan . serializers import PlanSerializer
    DEPOSITSERIALIZER = DepositSerializer
    WITHDRAWALSERIALIZER = WithdrawalSerializer
    deposits = DEPOSITSERIALIZER(many=True,source="validated_deposits")
    withdrawals = WITHDRAWALSERIALIZER(many=True,source="validated_withdrawals")
    plan = PlanSerializer()
    class Meta:
        model = User
        exclude = ['password']
        
    def get_deposits(self, obj): 
        deposits = obj.validated_deposits.order_by('-created_at')[:2]
        return self.DEPOSITSERIALIZER(deposits, many=True).data

    def get_withdrawals(self, obj):
        withdrawals = obj.validated_withdrawals.order_by('-created_at')[:2]
        return self.WITHDRAWALSERIALIZER(withdrawals, many=True).data


class PartialUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['image','plan'] 
        read_only_fields = ['id']

class UserDetailsSerializer(serializers.ModelSerializer):
    from account.serializers import DepositSerializer , WithdrawalSerializer
    from plan . serializers import PlanSerializer
    deposits = DepositSerializer(many=True,read_only=True)
    withdrawals = WithdrawalSerializer(many=True,read_only=True)
    plan = PlanSerializer()
    class Meta:
        model = User
        fields = '__all__'  # specify fields to include as needed