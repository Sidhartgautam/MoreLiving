from rest_framework import serializers
from .models import HouseRule

class HouseRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseRule
        fields = ['id', 'hotel', 'check_in_time', 'check_out_time', 'cancellation_policy', 'children_allowed', 'crib_policy', 'extra_bed_policy', 'age_restriction', 'age_restriction_details','additional_rules']
