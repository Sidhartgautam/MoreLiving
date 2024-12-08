from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Room, RoomType, RoomImage, RoomAmenities
from .serializers import RoomSerializer, RoomTypeSerializer, RoomImageSerializer, RoomAmenitiesSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from core.utils.filters.roomfilter import RoomFilter, RoomTypeFilter, RoomImageFilter, RoomAmenitiesFilter

# Create your views here.
class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Room created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Room creation failed",
                data=serializer.errors
            )
            return response.send(400)

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoomFilter
    search_fields = ['room_number', 'floor']

    def get_queryset(self):
        user = self.request.user
        hotel = user.hotel_set.first()
        return Room.objects.filter(hotel=hotel) if hotel else Room.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
             success=True,
             message="Room list retrieved successfully",
             data=serializer.data
         )
        return response.send()
        
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Room list retrieved successfully",
            data=serializer.data
        )
        return response.send()

class RoomTypeCreate(generics.CreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Room type created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Room type creation failed",
                data=serializer.errors
            )
            return response.send(400)

class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomTypeFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Room type list retrieved successfully",
            data=serializer.data
        )
        return response.send()


class RoomImageCreate(generics.CreateAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Room image created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Room image creation failed",
                data=serializer.errors
            )
            return response.send(400)

class RoomImageListView(generics.ListAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomImageFilter

    def get_queryset(self):
        user = self.request.user
        hotel = user.hotel_set.first()
        return RoomImage.objects.filter(room__hotel=hotel) if hotel else RoomImage.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Room image list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
        

class RoomAmenitiesCreate(generics.CreateAPIView):
    queryset = RoomAmenities.objects.all()
    serializer_class = RoomAmenitiesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Room amenities created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Room amenities creation failed",
                data=serializer.errors
            )
            return response.send(400)

class RoomAmenitiesListView(generics.ListAPIView):
    queryset = RoomAmenities.objects.all()
    serializer_class = RoomAmenitiesSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomAmenitiesFilter

    def get_queryset(self):
        user = self.request.user
        hotel = user.hotel_set.first()
        return RoomAmenities.objects.filter(room__hotel=hotel) if hotel else RoomAmenities.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = PrepareResponse(
                success=True,
                message="Room amenities list retrieved successfully",
                data=serializer.data
            )
            return response.send()
        
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Room amenities list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)

