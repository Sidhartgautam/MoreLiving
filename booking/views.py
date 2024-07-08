from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Booking, BookingStatus
from .serializers import BookingSerializer, BookingStatusSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from django.core.exceptions import ValidationError

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                response = PrepareResponse(
                    success=True,
                    message="Booking created successfully",
                    data=serializer.data
                )
                return response.send(code=status.HTTP_201_CREATED)
            except ValidationError as e:
                response = PrepareResponse(
                    success=False,
                    message=str(e),
                    data={}
                )
                return response.send(code=status.HTTP_400_BAD_REQUEST)
        else:
            response = PrepareResponse(
                success=False,
                message="Booking creation failed",
                data=serializer.errors
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Booking list retrieved successfully",
            data=serializer.data
        )
        return response.send()
class BookingStatusListView(generics.ListAPIView):
    queryset = BookingStatus.objects.all()
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Booking status list retrieved successfully",
            data=serializer.data
        )
        return response.send()

class BookingCancelView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        reason = request.data.get('cancellation_reason', '')
        try:
            booking.cancel(reason)
            response = PrepareResponse(
                success=True,
                message="Booking cancelled successfully",
                data=BookingSerializer(booking).data
            )
            return response.send(code=status.HTTP_200_OK)
        except ValidationError as e:
            response = PrepareResponse(
                success=False,
                message=str(e),
                data={}
            )
            return response.send(code=status.HTTP_400_BAD_REQUEST)