from django.shortcuts import render
from .models import HouseRule
from .serializers import HouseRuleSerializer
from core.utils.response import PrepareResponse
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class HouseRuleCreateView(generics.GenericAPIView):
    serializer_class = HouseRuleSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                message="House rule created successfully",
                data=serializer.data
            )
            return response.send(200)
        else:
            response = PrepareResponse(
                success=False,
                message="House rule creation failed",
                data=serializer.errors
            )
            return response.send(400)
        
class HouseRuleListView(generics.GenericAPIView):
    serializer_class = HouseRuleSerializer
    def get(self, request, *args, **kwargs):
        house_rules = HouseRuleSerializer(HouseRule.objects.all(), many=True)
        response = PrepareResponse(
            success=True,
            message="House rules fetched successfully",
            data=house_rules.data
        )
        return response.send(200)
