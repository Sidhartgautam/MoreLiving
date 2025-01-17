from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hotel, HotelType, HotelFacility, HotelImage,PropertyType
from country.models import City
from rest_framework import generics
from .serializers import (
    PropertyTypeSerializer,
    HotelSerializer, 
    HotelTypeSerializer, 
    HotelFacilitySerializer, 
    HotelImageSerializer,
    HotelDetailSerializer,
    TrendingDestinationSerializer
)
from rest_framework import permissions
from rest_framework import status
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from core.utils.filters.hotelfilter import HotelFilter, HotelTypeFilter, HotelFacilityFilter, HotelImageFilter,HotelSearchFilter

# Create your views here.

class PropertyTypeListView(generics.ListAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Property types retrieved successfully",
            data=serializer.data
        ).send(200)

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

class HotelListView(generics.GenericAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)

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
    
class HotelFacilityCreateView(generics.CreateAPIView):
    queryset = HotelFacility.objects.all()
    serializer_class = HotelFacilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Hotel facility created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Hotel facility creation failed",
                data=serializer.errors
            )
            return response.send(400)

class HotelFacilityListView(generics.ListAPIView):
    serializer_class = HotelFacilitySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelFacilityFilter
    search_fields = ['hotel__hotel_name', 'facility_name']

    def get_queryset(self):
        return HotelFacility.objects.filter(hotel__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel facility list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    
class HotelImageCreateView(generics.CreateAPIView):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="Hotel image uploaded successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response = PrepareResponse(
                success=False,
                message="Hotel image upload failed",
                data=serializer.errors
            )
            return response.send(400)

class HotelImageListView(generics.ListAPIView):
    serializer_class = HotelImageSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelImageFilter
    search_fields = ['hotel__hotel_name']

    def get_queryset(self):
        return HotelImage.objects.filter(hotel__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel image list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    

class HotelSearchView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelSearchFilter
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer

    def get(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id') 
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return PrepareResponse(
                success=False,
                message="Hotel not found",
                data=None
            ).send(404)

        serializer = self.get_serializer(hotel)
        return PrepareResponse(
            success=True,
            message="Hotel details retrieved successfully",
            data=serializer.data
        ).send(200)
    
class TrendingDestinationsView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        cities = City.objects.annotate(
            hotel_count=Count('hotels')  
        ).order_by('-hotel_count')[:6] 

        serializer = TrendingDestinationSerializer(cities, many=True)
        return PrepareResponse(
            success=True, 
            message="Trending destinations retrieved successfully", 
            data=serializer.data
        ).send(200)
    
class HotelsByPropertyTypeView(generics.ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        property_type_id = self.kwargs.get('property_type_id')
        return Hotel.objects.filter(property_type__id=property_type_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Hotels by property type retrieved successfully",
            data=serializer.data
        ).send(200)
    
