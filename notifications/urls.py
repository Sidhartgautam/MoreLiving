from django.urls import path 
from .views import NotificationListView, NotificationUpdateView

urlpatterns=[
    path('notifications/', NotificationListView.as_view()),
    path('notifications/<uuid:pk>/read/', NotificationUpdateView.as_view()),
]