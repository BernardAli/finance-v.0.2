from django.contrib import admin
from .models import Inflation, MPR, T_BILL, Security, CurrencyPair, InterbankFX

# Register your models here.

admin.site.register(Inflation)
admin.site.register(MPR)


@admin.register(T_BILL)
class T_BILLAdmin(admin.ModelAdmin):
    list_display = ('issue_date', 'tender', 'security', 'discount', 'interest')
    list_filter = ('tender', 'issue_date')


@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    list_display = ('id', 'security', 'slug')


@admin.register(InterbankFX)
class InterbankFXAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'pair', 'buying', 'selling')
    list_filter = ('pair',)


@admin.register(CurrencyPair)
class CurrencyPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'pair', 'currency')
