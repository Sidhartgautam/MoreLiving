from rest_framework import generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Review
from .serializers import ReviewSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from core.utils.filters.reviewfilter import ReviewFilter


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class =ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request,*args, **kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response=PrepareResponse(
                success = True,
                message="Review created successfully",
                data=serializer.data
            )
            return response.send(code=status.HTTP_201_CREATED)
        else:
            response=PrepareResponse(
                success = False,
                message="Review creation failed",
                data=serializer.errors
            )
            return response.send(400)
        
class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ['hotel__hotel_name', 'user__username', 'rating']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    def list(self,request,*args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Review list retrieved successfully",
            data=serializer.data
        )
        return response.send()

