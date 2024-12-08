from rest_framework import generics, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.views import APIView
import stripe
import requests
from django.conf import settings
from core.utils.moredealstoken import get_moredeals_token
from core.utils.booking import calculate_booking_price

from rest_framework.permissions import IsAuthenticated

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookingCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BookingSerializer(data=data, context={'request': request})

        if not serializer.is_valid():
            return PrepareResponse(
                success=False,
                data=serializer.errors,
                message="Booking creation failed"
            ).send(status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        total_price = calculate_booking_price(validated_data)

        try:
            with transaction.atomic():
                booking = serializer.save(user=request.user)
                payment_status, message = self.process_payment(
                    request=request,
                    payment_method=validated_data.get('payment_method'),
                    amount=total_price,
                    user=request.user,
                    booking=booking
                )

                if payment_status == 'Paid':
                    return PrepareResponse(
                        success=True,
                        message="Booking created successfully.",
                        data=serializer.data
                    ).send(status.HTTP_201_CREATED)
                else:
                    return PrepareResponse(
                        success=False,
                        message=message,
                        data={}
                    ).send(status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return PrepareResponse(
                success=False,
                message="Booking creation failed",
                errors={"payment_errors": str(e)}
            ).send(status.HTTP_400_BAD_REQUEST)

    def process_payment(self, request, payment_method, amount, user, booking):
        """
        Handles payment processing for different methods.
        """
        if payment_method == 'cod':
            booking.status = 'pending'
            booking.save()
            return 'Unpaid', "Booking placed with Cash on Delivery."
        elif payment_method == 'stripe':
            return self.process_stripe_payment(request, amount)
        elif payment_method == 'moredeals':
            return self.process_moredeals_payment(request, amount)
        else:
            raise ValidationError("Unsupported payment method.")

    def process_stripe_payment(self, request, amount):
        try:
            payment_method_id = request.data.get('payment_method_id')
            if not payment_method_id:
                raise ValidationError("Payment method ID not provided.")
            
            payment_intent = stripe.PaymentIntent.confirm(payment_method_id)
            if payment_intent['status'] != 'succeeded':
                raise ValidationError(f"Payment failed with status: {payment_intent['status']}")
            return 'Paid', "Stripe payment successful."
        except stripe.error.CardError as e:
            raise ValidationError(str(e))

    def process_moredeals_payment(self, request, amount):
        pin = request.data.get('pin')
        if not pin:
            raise ValidationError("PIN not provided for MoreDeals payment.")

        access_token = get_moredeals_token(request)
        response = requests.post(
            "https://moretrek.com/api/payments/payment-through-balance/",
            json={'amount': float(amount), 'pin': pin, 'platform': 'MoreLiving'},
            headers={'Authorization': f"Bearer {access_token}"}
        )

        if response.status_code == 200:
            return 'Paid', "MoreDeals payment successful."
        else:
            errors = response.json().get('errors', 'Unknown error')
            return 'Unpaid', f"MoreDeals payment failed: {errors}"

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        hotel = self.request.user.hotel_set.first()
        return Booking.objects.filter(hotel=hotel) if hotel else Booking.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
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
        return response.send(200)


class BookingCancelView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hotel = self.request.user.hotel_set.first()
        return Booking.objects.filter(hotel=hotel) if hotel else Booking.objects.none()

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
