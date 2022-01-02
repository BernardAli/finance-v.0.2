from django.shortcuts import render
from .models import Inflation, MPR, InterbankFX, T_BILL

# Create your views here.


def inflation_view(request):
    inflation = Inflation.objects.all().order_by('month')

    context = {
        'inflation': inflation,
    }
    return render(request, 'inflation.html', context)


def mpr_view(request):
    mprs = MPR.objects.all()

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
    t_bill = T_BILL.objects.all()

    context = {
        't_bill': t_bill,
    }
    return render(request, 't_bill.html', context)

