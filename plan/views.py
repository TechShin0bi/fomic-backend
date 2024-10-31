from datetime import timedelta
from rest_framework import generics, permissions,status
from .models import Plan,UserPlan
from rest_framework.permissions import IsAuthenticated
from .serializers import PlanSerializer,UserPlanSerializer
from rest_framework.response import Response
from django.utils.timezone import now
from .models import UserPlan
from rest_framework.views import APIView
from django.db.models import F, ExpressionWrapper, DateTimeField


class PlanListCreateView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class UserPlanListCreateView(generics.ListCreateAPIView):
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    # def perform_create(self, serializer):
    #     # Automatically set the user to the authenticated user
    #     serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Prepare the data and include the authenticated user's ID
        data = request.data
        data['user'] = request.user.id  # Use the user instance directly

        # Delete any previous user plans for this user
        UserPlan.objects.filter(user=request.user.id).delete()

        # Initialize the serializer with the request data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)  # Ensure the data is valid

        # Save the new UserPlan and get the instance
        user_plan = serializer.save()

        # Fetch the associated Plan instance from the created UserPlan
        plan = user_plan.plan  # Access the related plan object

        # Serialize the response data (including UserPlan and Plan)
        response_data = {
            "user_plan": UserPlanSerializer(user_plan).data,
            "plan": PlanSerializer(plan).data,  # Assuming you have a PlanSerializer
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    
class UserActivePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Query the user's active plan through UserPlan model
        active_plan = (
            UserPlan.objects.filter(user=request.user,is_active=True)
            .order_by("-updated_at")
            .select_related('plan')  # Optimize query with related plan
            .first()
        )

        if active_plan:
            plan = active_plan.plan
            data = {
                "name": plan.name,
                "price": float(plan.price),
                "daily_revenue": float(plan.daily_revenue),
                "duration": plan.duration,
                "category": plan.get_category_display(),
                "created_at": plan.created_at,
                "updated_at": plan.updated_at,
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "No active plan found."}, status=status.HTTP_404_NOT_FOUND
        )
        

        
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
            user = user_plan.user

            if days_passed <= 0:
                return Response(
                    {"message": "No days passed since the last process.", "new_balance": user.balance,},
                    status=status.HTTP_200_OK,
                )

            # Calculate the accumulated amount
            daily_revenue = plan.daily_revenue
            accumulated_amount = daily_revenue * days_passed

            # Update user's balance
            user.balance += accumulated_amount  # Assuming `balance` field exists on User model
            user.save()

            # Update last_process date to today
            user_plan.last_process = now()
            user_plan.save()
            
            # Calculate referral bonus
            user_plan.calculate_referral_bonus()
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