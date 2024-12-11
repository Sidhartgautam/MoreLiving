from django.urls import path
from .views import OfferListView, OfferDetailView, OfferCreateView

urlpatterns = [
    path('offers/lists/', OfferListView.as_view(), name='offer-list'),
    path('offers/create/', OfferCreateView.as_view(), name='offer-create'),
    path('offers/<uuid:offer_id>/', OfferDetailView.as_view(), name='offer-detail'),
]