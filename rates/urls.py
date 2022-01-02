from django.urls import path
from .views import inflation_view, mpr_view, fx_view, treasury_bill_view

urlpatterns = [
    path('inflation/', inflation_view, name='inflation'),
    path('mpr/', mpr_view, name='mpr'),
    path('fx/', fx_view, name='fx'),
    path('t_bill/', treasury_bill_view, name='t_bill'),
]