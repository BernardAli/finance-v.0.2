from django.contrib import admin
from .models import Continent, Country, Indice, Commodity_type, Commodity_profile, President, CentralBank, BankRate, \
    Bourse, MajorExports, UnemploymentRate, GDP, Population

# Register your models here.

admin.site.register(Continent)
admin.site.register(President)
admin.site.register(Population)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital', 'continent')
    list_filter = ('continent', 'time_zone', 'currency')
    ordering = ('name',)
    search_fields = ('name', 'capital', 'continent')


@admin.register(Indice)
class IndiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'country')
    list_filter = ('country',)
    ordering = ('country', 'name')


@admin.register(Bourse)
class BourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('country',)


admin.site.register(Commodity_type)
admin.site.register(Commodity_profile)


@admin.register(CentralBank)
class CentralBankAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(BankRate)
admin.site.register(MajorExports)
admin.site.register(UnemploymentRate)


@admin.register(GDP)
class GDPAdmin(admin.ModelAdmin):
    list_display = ('country', 'value')
