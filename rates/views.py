from datetime import timedelta

from django.shortcuts import render
from .models import Inflation, MPR, InterbankFX, T_BILL

# Create your views here.


def inflation_view(request):
    inflation = Inflation.objects.all().order_by('-month')
    inflation_chart = Inflation.objects.all().order_by('-month')[:12]
    inflation_previous = Inflation.objects.all().order_by('-month')[1]

    context = {
        'inflation': inflation,
        'inflation_chart': inflation_chart,
        'inflation_previous': inflation_previous,
    }
    return render(request, 'inflation.html', context)


def mpr_view(request):
    mprs = MPR.objects.all().order_by("-meeting_no")

    context = {
        'mprs': mprs,
    }
    return render(request, 'mpr.html', context)


def fx_view(request):
    fx = InterbankFX.objects.all()

    context = {
        'fx': fx,
    }
    return render(request, 'fx.html', context)


def treasury_bill_view(request):
    t_bill = T_BILL.objects.order_by('-issue_date')
    three_months = T_BILL.objects.filter(security=1).order_by('-issue_date')
    six_months = T_BILL.objects.filter(security=2).order_by('-issue_date')
    share_price_first = T_BILL.objects.filter(security=1).order_by('issue_date').first()
    share_price_latest = T_BILL.objects.filter(security=1).order_by('issue_date').last()

    context = {
        't_bill': t_bill,
        'three_months': three_months,
        'six_months': six_months,
        'share_price_latest': share_price_latest,
        'one_month': share_price_latest.issue_date - timedelta(weeks=4),
        'six_month': share_price_latest.issue_date - timedelta(weeks=26),
        'one_year': share_price_latest.issue_date - timedelta(weeks=52),
        'share_price_first': share_price_first.issue_date,

        'nine_one_month': share_price_latest.issue_date - timedelta(weeks=4),
        'nine_six_month': share_price_latest.issue_date - timedelta(weeks=26),
        'nine_one_year': share_price_latest.issue_date - timedelta(weeks=52),
    }
    return render(request, 't_bill.html', context)

