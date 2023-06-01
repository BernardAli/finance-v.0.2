from django.urls import path
from .views import fixed_income_view

urlpatterns = [
    path('', fixed_income_view, name='fixed_income'),
]
