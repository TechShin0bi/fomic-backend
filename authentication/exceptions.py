from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

class UserInactiveException(PermissionDenied):
    """Custom exception for inactive users."""
    pass

def custom_permission_denied_view(request, exception):
    """Custom handler for 403 Forbidden errors."""
    return JsonResponse({'error': str(exception)}, status=403)
