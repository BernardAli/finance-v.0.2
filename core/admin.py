from django.contrib import admin
from .models import Tag, Sector, CompanyProfile, Market, ShareDetail, SharePrice, \
    Indices, FinancialPeriod, Report, MarketReport, PressRelease, Subsidiaries, \
    Auditors, Secretary, KeyPeople, IPO, Dividend, Registrar, Solicitor, Ownership, Opinions, \
    FinancialStatement, Review, AuditingServices, Products, ShareSplit, GCX_Types, ShareType, \
    EconomicCalendar, AGM, Brand, OperatingSegment, Advertisement, BankHealth


# Register your models here.

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'sector')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_id', 'country', 'id')
    list_filter = ('index', 'sector', 'industry', 'country', 'share_type', 'market')
    search_fields = ['name', 'company_id', ]
    ordering = ('name',)


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('company', 'shareholder_name', 'shares_owned', 'percentage_holding')
    list_filter = ('company', 'date')
    search_fields = ['company', 'shareholder_name']
    ordering = ('company', '-shares_owned', 'shareholder_name',)


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'date')
    list_filter = ('company',)
    ordering = ('company', '-date')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Market)
admin.site.register(Review)
admin.site.register(AuditingServices)
admin.site.register(Products)
admin.site.register(ShareSplit)
admin.site.register(GCX_Types)
admin.site.register(EconomicCalendar)
admin.site.register(AGM)
admin.site.register(Brand)
admin.site.register(OperatingSegment)
admin.site.register(Advertisement)
admin.site.register(BankHealth)


@admin.register(ShareDetail)
class ShareDetailAdmin(admin.ModelAdmin):
    list_display = ('company', 'issued_shares', 'listed_date', 'financial_period_ends')
    list_filter = ('financial_period_ends', 'company__market', 'status')
    search_fields = ('company__name',)


@admin.register(SharePrice)
class SharePriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'date', 'price', 'volume')
    list_filter = ('date', 'company')


@admin.register(Indices)
class IndicesAdmin(admin.ModelAdmin):
    list_display = ('index', 'date', 'value')
    list_filter = ('index',)


admin.site.register(FinancialPeriod)
admin.site.register(FinancialStatement)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('year', 'period', 'company')
    list_filter = ('year', 'company')
    search_fields = ('year', 'company__name')


@admin.register(MarketReport)
class MarketReportAdmin(admin.ModelAdmin):
    list_display = ('session_number', 'date')
    list_filter = ('date',)


@admin.register(Auditors)
class AuditorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'telephone', 'incorporated_date')


admin.site.register(Secretary)


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    list_display = ('position', 'name')
    list_filter = ('position', 'company')


admin.site.register(IPO)


@admin.register(Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ('company', 'final_dividend', 'payment_date')
    list_filter = ('company__company_id', )


admin.site.register(Registrar)
admin.site.register(Solicitor)
admin.site.register(Subsidiaries)
admin.site.register(Opinions)
admin.site.register(ShareType)
