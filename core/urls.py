from django.urls import path
from .views import index_view, about_view, listed_companies, company_details, sector, market, stock_market_view, \
    industry_view, auditor_detail, company_summary, career_view, company_dividend_details, company_press_details, \
    SearchResultsListView

urlpatterns = [
    path('', index_view, name='index'),
    path('stock_market/', stock_market_view, name='stock_market'),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path('companies/', listed_companies, name='listed_companies'),
    path('companies/<uuid:company_id>', company_details, name='company_details'),
    path('companies/<uuid:company_id>/dividend/', company_dividend_details, name='company_dividend_details'),
    path('companies/<uuid:company_id>/press/', company_press_details, name='company_press_details'),
    path('auditor/<int:auditor_id>', auditor_detail, name='auditor'),
    path('sector/<sector_slug>', sector, name='sector'),
    path('market/<market_slug>', market, name='market'),
    path('tag/<slug:tag_slug>', industry_view, name='industry'),
    path('summary/', company_summary, name='summary'),
    path('about/', about_view, name='about'),
    path('career/', career_view, name='career'),
]