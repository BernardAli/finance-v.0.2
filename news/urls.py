from django.urls import path
from .views import news_list, news_details, news_tags


urlpatterns = [
    path('', news_list, name='news_list'),
    path('<int:news_id>/', news_details, name='news_details'),
    path('tag/<slug:tag_slug>', news_tags, name='tags'),
]