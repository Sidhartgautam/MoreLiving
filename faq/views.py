from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import HotelFAQ,WebsiteFAQ
from .serializers import HotelFAQSerializer,WebsiteFAQSerializer
from rest_framework import generics
from rest_framework import permissions
from core.utils.response import PrepareResponse

# Create your views here.

class HotelFAQCreateView(generics.GenericAPIView):
    queryset = HotelFAQ.objects.all()
    serializer_class = HotelFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hotel=self.request.user.hotel)
        return PrepareResponse(
            success=True,
            message="Hotel FAQ created successfully",
            data=serializer.data
        ).send(200)


class HotelFAQView(generics.GenericAPIView):
    queryset = HotelFAQ.objects.all()
    serializer_class = HotelFAQSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(hotel=self.request.user.hotel)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel FAQ list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
    
    

class WebsiteFAQCreateView(generics.GenericAPIView):
    queryset = WebsiteFAQ.objects.all()
    serializer_class = WebsiteFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return PrepareResponse(
            success=True,
            message="Website FAQ created successfully",
            data=serializer.data
        ).send(200)

class WebsiteFAQView(generics.GenericAPIView):
    queryset = WebsiteFAQ.objects.all()
    serializer_class = WebsiteFAQSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Website FAQ list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
  