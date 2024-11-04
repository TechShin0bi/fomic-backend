
from rest_framework.pagination import PageNumberPagination

class ReferralPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set a custom page size
    max_page_size = 100  # Maximum page size that can be set