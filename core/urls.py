from django.urls import path
from .views import index_view, about_view, listed_companies, company_details, sector, market, stock_market_view, \
    industry_view, auditor_detail, company_summary, career_view, company_dividend_details, company_press_details, \
    SearchResultsListView, review_edit, opinions_details, registrar_detail, market_detail, company_file, gcx_home, share_type_detail, share_type_detail_perfomance

urlpatterns = [
    path('', index_view, name='index'),
    path('stock_market/', stock_market_view, name='stock_market'),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path('companies/', listed_companies, name='listed_companies'),
    path('companies/<uuid:company_id>', company_details, name='company_details'),
    path('company_file/<uuid:company_id>', company_file, name='company_file'),
    path('companies/<uuid:company_pk>/reviews/new/', review_edit, name='review_create'),
    path('companies/<uuid:company_pk>/reviews/<int:review_pk>/', review_edit, name='review_edit'),
    path('companies/<uuid:company_id>/dividend/', company_dividend_details, name='company_dividend_details'),
    path('companies/<uuid:company_id>/press/', company_press_details, name='company_press_details'),
    path('auditor/<int:auditor_id>', auditor_detail, name='auditor'),
    path('registrar/<int:registrar_id>', registrar_detail, name='registrar'),
    path('opinions_details/<int:opinions_id>', opinions_details, name='opinions_details'),
    path('sector/<sector_slug>', sector, name='sector'),
    path('market/<market_slug>', market, name='market'),
    path('share_type_detail/<share_type_id>', share_type_detail, name='share_type_detail'),
    path('market_detail/<market_slug>', market_detail, name='market_detail'),
    path('share_type_detail_perfomance/<share_type_id>', share_type_detail_perfomance, name='share_type_detail_perfomance'),
    path('tag/<slug:tag_slug>', industry_view, name='industry'),
    path('summary/', company_summary, name='summary'),
    path('about/', about_view, name='about'),
    path('career/', career_view, name='career'),
    path('gcx_home/', gcx_home, name='gcx_home'),
]