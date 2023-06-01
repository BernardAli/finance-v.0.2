from django.shortcuts import render

# Create your views here.


def bonds_view(request):
    return render(request, 'bonds/bonds_market.html')