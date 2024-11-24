from django.urls import path
from .views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('list/', ReviewListView.as_view(), name='review-list'),
]