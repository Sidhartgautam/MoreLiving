from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import HotelReview, GuestReview
from .serializers import HotelReviewSerializer, GuestReviewSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from core.utils.filters.reviewfilter import HotelReviewFilter, GuestReviewFilter

class HotelReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = PrepareResponse(
            success=True,
            message="Review created successfully",
            data=serializer.data
        )
        return response.send(200)
class HotelReviewListView(generics.ListAPIView):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelReviewFilter
    search_fields = ['hotel__hotel_name']
    ordering_fields = ['hotel__hotel_name']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Hotel review list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    

class GuestReviewListView(generics.ListAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GuestReviewFilter
    search_fields = ['guest__first_name', 'guest__last_name']
    ordering_fields = ['guest__first_name', 'guest__last_name']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Guest review list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    
class GuestReviewCreateView(generics.CreateAPIView):
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = PrepareResponse(
            success=True,
            message="Guest review created successfully",
            data=serializer.data
        )
        return response.send()

