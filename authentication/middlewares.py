from django.core.exceptions import PermissionDenied

class UserInactiveException(PermissionDenied):
    """Custom exception to be raised when the user's account is inactive."""
    pass

class CheckActiveUserMiddleware:
    """
    Middleware to check if the user is active. If not, raise an exception.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check if the user is authenticated
        if request.user.is_authenticated:
            if not request.user.is_active:
                # Raise a custom exception when the user is inactive
                raise UserInactiveException("Your account is inactive. Please contact support.")

        # Proceed with the response if the user is active
        response = self.get_response(request)
        return response
