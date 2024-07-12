from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id','hotel','user','rating','comment','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at','user']

    def create(self,validated_data):
        review =Review.objects.create(user=self.context['request'].user,**validated_data)
        return review