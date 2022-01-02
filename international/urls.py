from django.urls import path
from .views import country, continent, index_detail, index_list, commodity_list, commodity_profile, commodity_detail

urlpatterns = [
    path('continent/<continent_slug>', continent, name='continent'),
    path('country/<country_slug>', country, name='country'),
    path('index/', index_list, name='index_list'),
    path('index/<int:index_id>', index_detail, name='index_detail'),
    path('commodity/', commodity_list, name='commodity_list'),
    path('commodity/<int:commodity_id>', commodity_detail, name='commodity_detail'),
    path('commodity/<commodity_slug>', commodity_profile, name='commodity_profile'),
]