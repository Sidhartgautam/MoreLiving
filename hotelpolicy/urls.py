from django.urls import path
from .views import HouseRuleListView

urlpatterns = [
    path('house_rules/', HouseRuleListView.as_view(), name='house_rule-list'),
]