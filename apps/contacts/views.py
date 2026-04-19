from rest_framework import viewsets, permissions
from .models import ContactInquiry
from .serializers import ContactInquirySerializer
from core.cache import RedisCacheMixin

class ContactInquiryViewSet(RedisCacheMixin, viewsets.ModelViewSet):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer

    def get_permissions(self):
        # Public users can POST (submit) a contact inquiry
        if self.action == 'create':
            return [permissions.AllowAny()]
        
        # Only Admins mapping to a valid JWT can GET, UPDATE, or DELETE the list of inquiries 
        return [permissions.IsAuthenticated()]
