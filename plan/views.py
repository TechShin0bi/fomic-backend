from rest_framework import generics
from .models import Plan,UserPlan
from .serializers import PlanSerializer,UserPlanSerializer
from rest_framework.response import Response
from django.utils.timezone import now
from .models import UserPlan
from rest_framework import generics, status

# List all plans or create a new one
class PlanListCreateView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

# Retrieve, update, or delete a specific plan
class PlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

# List all user plans or create a new one
class UserPlanListCreateView(generics.ListCreateAPIView):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

# Retrieve, update, or delete a specific user plan
class UserPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

class UpdateUserPlanView(generics.GenericAPIView):
    """
    View to calculate and update the user's balance based on the daily revenue and days passed.
    """
    def get(self, request, user_id):
        try:
            # Retrieve the active plan of the user
            user_plan = UserPlan.objects.get(user__id=user_id, is_active=True)
            plan = user_plan.plan  # Fetch the linked plan

            # Calculate the number of days since the last process
            days_passed = (now().date() - user_plan.last_process.date()).days

            if days_passed <= 0:
                return Response(
                    {"message": "No days passed since the last process."},
                    status=status.HTTP_200_OK,
                )

            # Calculate the accumulated amount
            daily_revenue = plan.daily_revenue
            accumulated_amount = daily_revenue * days_passed

            # Update user's balance
            user = user_plan.user
            user.balance += accumulated_amount  # Assuming `balance` field exists on User model
            user.save()

            # Update last_process date to today
            user_plan.last_process = now()
            user_plan.save()

            return Response(
                {
                    "message": "User plan updated successfully.",
                    "days_passed": days_passed,
                    "accumulated_amount": accumulated_amount,
                    "new_balance": user.balance,
                },
                status=status.HTTP_200_OK,
            )

        except UserPlan.DoesNotExist:
            return Response(
                {"error": "Active user plan not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )