from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hotel, HotelType
from rest_framework import generics
from .serializers import HotelSerializer, HotelTypeSerializer
from rest_framework import permissions
from rest_framework import status
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from core.utils.filters.hotelfilter import HotelFilter, HotelTypeFilter

# Create your views here.

class HotelCreateView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = PrepareResponse(
                success=True,
                message="Hotel created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Hotel creation failed",
                data=serializer.errors
            )
            return response.send(400)

class HotelListView(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelFilter
    search_fields = ['hotel_name', 'city', 'state']

    def get_queryset(self):
        return Hotel.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel list retrieved successfully",
            data=serializer.data
        )
        return response.send()

class HotelTypeCreate(generics.CreateAPIView):
    queryset = HotelType.objects.all()
    serializer_class = HotelTypeSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response = PrepareResponse(
                success=True,
                message="Hotel type created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Hotel type creation failed",
                data=serializer.errors
            )
            return response.send(400)

class HotelTypeList(generics.ListAPIView):
    queryset = HotelType.objects.all()
    serializer_class = HotelTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelTypeFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel type list retrieved successfully",
            data=serializer.data
        )
        return response.send()
