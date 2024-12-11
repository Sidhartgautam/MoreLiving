from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.HotelCreateView.as_view()),
    path('hotels/list/', views.HotelListView.as_view()),
    path('hotels/type/', views.HotelTypeCreate.as_view()),
    path('hotels/type/list/', views.HotelTypeList.as_view()),
    path('search/', views.HotelSearchView.as_view(), name='hotel-search'),
    path('hotels/facilities/',views.HotelFacilityCreateView.as_view(), name='hotel-facility-create'),
    path('hotels/facilities/list/',views.HotelFacilityListView.as_view(), name='hotel-facility-list'),
    path('hotels/images/',views.HotelImageCreateView.as_view(), name='hotel-image-create'),
    path('hotels/images/list/',views.HotelImageListView.as_view(), name='hotel-image-list'),
    path('hotels/<uuid:hotel_id>/details/', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('top-trending/', views.TrendingDestinationsView.as_view(), name='trending-destinations'),
]