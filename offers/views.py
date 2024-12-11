from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Offer
from .serializers import OfferSerializer
from core.utils.response import PrepareResponse
from rest_framework import permissions


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

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = PrepareResponse(
            success=True,
            message="Offer list retrieved successfully",
            data=serializer.data
        )
        return response.send(200)
    
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
    