from rest_framework import generics, status
from .models import Plan
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from authentication.serializers import UserSerializer
from . serializers import PlanSerializer
from authentication.serializers import GetUserSerializer
User = get_user_model()

class PlanListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    def create(self, request, *args, **kwargs):
            data = request.data.copy()
            user = request.user  # Authenticated user
            if user.plan:
                # If user already has a UserPlan, update it with the new plan
                user.plan_id = data.get('plan')  # Expecting 'plan' to be in request data
                user.save(update_fields=['plan'])
            else:
                # If no UserPlan exists, create a new one
                data['user'] = user.id  # Associate the UserPlan with the authenticated user
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

            # Update the `plan` field in the User model
            user.plan = user.plan
            user.save(update_fields=['plan'])  # Only update the `plan` field

            # Return updated user data
            response_data = UserSerializer(user).data  # Serializes complete user data, including plan details

            return Response(response_data)

        
class UpdateUserPlanView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    """
    View to calculate and update the user's balance based on the daily revenue and days passed.
    This also updates the plans of any referred users.
    """
    def get(self, request):
        try:
            # Retrieve the user instance
            user = request.user

            # Call the method to update balance and referred users
            user.update_balance_and_referred_users()

            return Response(GetUserSerializer(user).data,
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
        

class CreatePlansView(APIView):
    def post(self, request, *args, **kwargs):
        plans_part1 = [
            {"name": "VIP 1", "price": 5000, "daily_revenue": 355, "duration": 90, "category": "1"},
            {"name": "VIP 2", "price": 10000, "daily_revenue": 710, "duration": 90, "category": "1"},
            {"name": "VIP 3", "price": 12000, "daily_revenue": 852, "duration": 90, "category": "1"},
            {"name": "VIP 4", "price": 20000, "daily_revenue": 1420, "duration": 90, "category": "1"},
            {"name": "VIP 5", "price": 40000, "daily_revenue": 2840, "duration": 90, "category": "1"},
            {"name": "VIP 6", "price": 50000, "daily_revenue": 3550, "duration": 90, "category": "1"},
            {"name": "VIP 7", "price": 100000, "daily_revenue": 7100, "duration": 90, "category": "1"},
        ]

        plans_part2 = [
            {"name": "VIP 8", "price": 200000, "daily_revenue": 14200, "duration": 90, "category": "2"},
            {"name": "VIP 9", "price": 300000, "daily_revenue": 21300, "duration": 90, "category": "2"},
            {"name": "VIP 10", "price": 400000, "daily_revenue": 28400, "duration": 90, "category": "2"},
            {"name": "VIP 11", "price": 500000, "daily_revenue": 35500, "duration": 90, "category": "2"},
            {"name": "VIP 12", "price": 1000000, "daily_revenue": 71000, "duration": 90, "category": "2"},
            {"name": "VIP 13", "price": 2000000, "daily_revenue": 142000, "duration": 90, "category": "2"},
        ]

        plans = plans_part1 + plans_part2
        created_plans = []

        for plan in plans:
            created_plan = Plan.objects.create(**plan)
            created_plans.append(created_plan)

        return Response({"message": "Plans created successfully"}, status=status.HTTP_201_CREATED)