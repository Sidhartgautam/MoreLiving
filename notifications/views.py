from rest_framework import generics,permissions,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Notification
from .serializers import NotificationSerializer
from core.utils.response import PrepareResponse
from core.utils.pagination.pagination import CustomPagination

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class =CustomPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['message', 'hotel__name']
    ordering_fields = ['created_at']
    def get_queryset(self):
        return Notification.objects.filter(hotel__user=self.request.user)
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        page =self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset,many=True)
        response = PrepareResponse(
            success=True,
            message="Notification list retrieved successfully",
            data=serializer.data
        )
        return response.send()
    
class NotificationUpdateView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class =NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
     
    def update(self, request, *args, **kwargs):
        notification =self.get_object()
        notification.is_read =True
        notification.save()
        serializer = self.get_serializer(notification)
        response = PrepareResponse(
            success=True,
            message="Notification updated successfully",
            data=serializer.data
        )
        return response.send(code = status.HTTP_200_OK)
