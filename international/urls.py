from django.urls import path
from .views import country, continent, index_detail, index_list, commodity_list, commodity_profile, commodity_detail, \
    SearchIndexListView, commodity_summary, index_summary

urlpatterns = [
    path('continent/<continent_slug>', continent, name='continent'),
    path('country/<country_slug>', country, name='country'),
    path("search_index/", SearchIndexListView.as_view(), name="search_index"),
    path('index/', index_list, name='index_list'),
    path('index_summary/', index_summary, name='index_summary'),
    path('index/<int:index_id>', index_detail, name='index_detail'),
    path('commodity/', commodity_list, name='commodity_list'),
    path('commodity_summary/', commodity_summary, name='commodity_summary'),
    path('commodity/<int:commodity_id>', commodity_detail, name='commodity_detail'),
    path('commodity/<commodity_slug>', commodity_profile, name='commodity_profile'),
]