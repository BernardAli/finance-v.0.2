from django.contrib import admin
from .models import Inflation, MPR, T_BILL, Security, CurrencyPair, InterbankFX

# Register your models here.

admin.site.register(Inflation)
admin.site.register(MPR)
admin.site.register(T_BILL)
admin.site.register(Security)
admin.site.register(CurrencyPair)
admin.site.register(InterbankFX)
