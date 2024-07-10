# country/views.py
from rest_framework import generics
from .models import Country
from .serializers import CountrySerializer
from core.utils.response import PrepareResponse
from rest_framework import permissions

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminUser]  # No authentication required

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Country list retrieved successfully",
            data=serializer.data
        )
        return response.send()
