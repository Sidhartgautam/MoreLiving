from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Offer
from .serializers import OfferSerializer
from datetime import datetime
from django.utils import timezone
from core.utils.response import PrepareResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils.dateparse import parse_date


# Create your views here.
class OfferCreateView(generics.GenericAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return PrepareResponse(
            success=True,
            message="Offer created successfully",
            data=serializer.data
        ).send(200)
    
class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hotel__city', 'hotel__hotel_name']
    ordering_fields = ['discount_percentage', 'valid_until']

    def get_queryset(self):
        queryset = self.queryset.filter(is_active=True)
        
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if start_date and end_date:
                queryset = queryset.filter(
                    valid_from__lte=end_date,
                    valid_until__gte=start_date
                )

        return queryset.order_by('-discount_percentage')
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response = PrepareResponse(
            success=True,
            message="Offer list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)


# class OfferListView(generics.ListAPIView):
#     queryset = Offer.objects.all()
#     serializer_class = OfferSerializer

#     def get_queryset(self):
#         return self.queryset.filter(is_active=True)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         response = PrepareResponse(
#             success=True,
#             message="Offer list retrieved successfully",
#             data=serializer.data
#         )
#         return response.send(200)
    
class OfferDetailView(generics.GenericAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        offer_id = self.kwargs('offer_id')
        return Offer.objects.filter(id=offer_id)

    def get(self, request, *args, **kwargs):
        offer_id = self.kwargs('offer_id')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Offer list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
    