from django.urls import path
from .views import bonds_view

urlpatterns = [
    path('', bonds_view, name='bonds'),
]
