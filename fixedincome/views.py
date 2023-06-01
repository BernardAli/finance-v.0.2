from django.shortcuts import render

# Create your views here.


def fixed_income_view(request):
    return render(request, 'fixed_income/income_market.html')