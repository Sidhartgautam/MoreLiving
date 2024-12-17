from rest_framework import generics, permissions
from .models import HotelFAQ, MoreLivingFAQ
from .serializers import HotelFAQSerializer, WebsiteFAQSerializer
from hotels.models import Hotel
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination


# Hotel FAQ Views
class HotelFAQCreateView(generics.GenericAPIView):
    serializer_class = HotelFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        hotel_id = self.kwargs.get('hotel_id')
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return PrepareResponse(success=False, message="Hotel not found").send(404)

        parent_id = request.data.get('parent')
        if parent_id:
            try:
                parent_faq = HotelFAQ.objects.get(id=parent_id, hotel=hotel)

                if parent_faq.parent is not None:
                    return PrepareResponse(success=False, message="Replies cannot have further replies").send(400)
                if request.user != hotel.user:
                    return PrepareResponse(success=False, message="Only hotel owner can add replies").send(403)
            except HotelFAQ.DoesNotExist:
                return PrepareResponse(success=False, message="Parent FAQ not found").send(404)
        else:
            parent_faq = None

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel, user=request.user, parent=parent_faq)
            return PrepareResponse(success=True, data=serializer.data, message="Hotel FAQ added").send(201)
        
        return PrepareResponse(success=False, data=serializer.errors, message="Failed to add FAQ").send(400)


class HotelFAQListView(generics.ListAPIView):
    serializer_class = HotelFAQSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return HotelFAQ.objects.filter(hotel_id=hotel_id, parent__isnull=True).order_by('-created_at')


# Website FAQ Views
class WebsiteFAQCreateView(generics.CreateAPIView):
    queryset = MoreLivingFAQ.objects.all()
    serializer_class = WebsiteFAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent_faq = MoreLivingFAQ.objects.filter(id=parent_id).first() if parent_id else None
        serializer.save(user=self.request.user, parent=parent_faq)


class WebsiteFAQListView(generics.ListAPIView):
    serializer_class = WebsiteFAQSerializer
    queryset = MoreLivingFAQ.objects.filter(parent__isnull=True).order_by('-created_at')
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]
