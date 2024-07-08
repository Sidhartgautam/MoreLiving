from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.HotelCreateView.as_view()),
    path('hotels/list/', views.HotelListView.as_view()),
    path('hotels/type/', views.HotelTypeCreate.as_view()),
    path('hotels/type/list/', views.HotelTypeList.as_view()),
]