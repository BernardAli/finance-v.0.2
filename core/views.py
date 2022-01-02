from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum
from rates.models import Inflation, MPR
from .models import Sector, Tag, CompanyProfile, Market, ShareDetail, SharePrice, Indices, Report, \
    MarketReport, PressRelease, Auditors, IPO, Dividend, Ownership, Registrar, Subsidiaries, Opinions
from news.models import News
from international.models import Continent, Indice, Commodity_type, BankRate, GDP, UnemploymentRate
# Create your views here.


def index_view(request):
    inflation = Inflation.objects.last()
    mpr = MPR.objects.last()
    sectors = Sector.objects.filter()
    markets = Market.objects.exclude(market='None')
    indices = Indices.objects.all()[:10]
    market_reports = MarketReport.objects.all().order_by('-session_number')[:5]
    news = News.objects.all().order_by('-date_posted')[:2]
    older_news = News.objects.all().order_by('-date_posted')[2:6]
    continents = Continent.objects.all().order_by('continent')
    indices = Indice.objects.all().order_by('-name')
    commodities = Commodity_type.objects.all().order_by('commodity_type')
    base_rates = BankRate.objects.all().distinct()[:5]
    gdp = GDP.objects.all().order_by('-value')[:10]
    unemployment = UnemploymentRate.objects.all().order_by('-value')[:10]
    release = PressRelease.objects.all().order_by('-date')[:5]
    opinions = Opinions.objects.all().order_by('-date')[:3]

    context = {
        'inflation': inflation,
        'mpr': mpr,
        'sectors': sectors,
        'markets': markets,
        'indices': indices,
        'market_reports': market_reports,
        'news': news,
        'older_news': older_news,
        'continents': continents,
        'indices': indices,
        'commodities': commodities,
        'base_rates': base_rates,
        'gdp': gdp,
        'unemployment': unemployment,
        'release': release,
        'opinions': opinions,
    }

    return render(request, 'index.html', context)


def listed_companies(request):
    companies = CompanyProfile.objects.all().order_by('company_id')

    context = {
        'companies': companies
    }
    return render(request, 'companies.html', context)


def company_details(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    share = ShareDetail.objects.filter(company_id=company_id)
    share_price = SharePrice.objects.filter(company_id=company_id)
    ipos = IPO.objects.filter(company_id=company_id)
    auditor = Auditors.objects.filter(company=company_id)
    reports = Report.objects.filter(company_id=company_id)
    dividends = Dividend.objects.filter(company_id=company_id).order_by('-register_closure')[:1]
    release = PressRelease.objects.filter(company_id=company_id).order_by('-date')[:5]
    price = SharePrice.objects.filter(company_id=company_id).last()
    ownership = Ownership.objects.filter(company_id=company_id).filter(date__year=2020 | 2021)
    percent_sum = Ownership.objects.aggregate(Sum('percentage_holding'))
    subsidiaries = Subsidiaries.objects.filter(company_id=company_id)
    # market_cap = price.price * share.issued_shares

    context = {
        'company': company,
        'share': share,
        'share_price': share_price,
        'reports': reports,
        'release': release,
        'auditor': auditor,
        'secretaries': company.secretary.all(),
        'key_people': company.key_people.all(),
        'price': price,
        'ipos': ipos,
        'dividends': dividends,
        'ownership': ownership,
        # 'market_cap': market_cap,
        "percent_sum": percent_sum,
        'registrars': company.registrar.all(),
        'subsidiaries': subsidiaries
    }
    return render(request, 'company_details.html', context)



def company_dividend_details(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    dividends = Dividend.objects.filter(company_id=company_id).order_by('-register_closure')

    context = {
        'company': company,
        'dividends': dividends
    }

    return render(request, 'company_dividend_details.html', context)


def company_press_details(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    release = PressRelease.objects.filter(company_id=company_id).order_by('-date')

    context = {
        'company': company,
        'release': release
    }

    return render(request, 'company_press_details.html', context)


def sector(request, sector_slug):
    sector = get_object_or_404(Sector, slug=sector_slug)
    companies = CompanyProfile.objects.filter(sector=sector).order_by('name')
    paginator = Paginator(companies, 50)

    sector_count = CompanyProfile.objects.filter(sector=sector).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sector': sector,
        'sector_count': sector_count,
    }
    return render(request, 'sectors.html', context)


def market(request, market_slug):
    market = get_object_or_404(Market, slug=market_slug)
    companies = CompanyProfile.objects.filter(market=market).order_by('name')
    paginator = Paginator(companies, 50)

    market_count = CompanyProfile.objects.filter(market=market).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'market': market,
        'market_count': market_count,
    }
    return render(request, 'market.html', context)


def stock_market_view(request):
    sectors = Sector.objects.all()
    markets = Market.objects.exclude(market='None')
    indices = Indices.objects.all()[:5]
    auditors = Auditors.objects.all()[:8]
    market_reports = MarketReport.objects.all().order_by('-session_number')[:5]

    companies_counts = CompanyProfile.objects.filter(country=1).count()

    context = {
        'sectors': sectors,
        'markets': markets,
        'indices': indices,
        'market_reports': market_reports,
        'auditors': auditors,
        'companies_counts': companies_counts,
    }

    return render(request, 'stock_market.html', context)


def industry_view(request, tag_slug):
    industry = get_object_or_404(Tag, slug=tag_slug)
    companies = CompanyProfile.objects.filter(industry=industry).order_by('company_id')

    paginator = Paginator(companies, 100)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    industry_count = CompanyProfile.objects.filter(industry=industry).count()

    context = {
        'page_obj': page_obj,
        'industry': industry,
        'industry_count': industry_count,
    }

    return render(request, 'industry.html', context)


def about_view(request):
    return render(request, 'about.html')


def career_view(request):
    return render(request, 'career.html')


def market(request, market_slug):
    market = get_object_or_404(Market, slug=market_slug)
    companies = CompanyProfile.objects.filter(market=market).order_by('name')
    paginator = Paginator(companies, 50)

    market_count = CompanyProfile.objects.filter(market=market).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'market': market,
        'market_count': market_count,
    }
    return render(request, 'market.html', context)


def company_summary(request):
    companies = CompanyProfile.objects.all().order_by('name')

    context = {
        'companies': companies
    }
    return render(request, 'company_summary.html', context)


def auditor_detail(request, auditor_id):
    auditor = get_object_or_404(Auditors, id=auditor_id)

    context = {
        'auditor': auditor
    }

    return render(request, 'auditor_details.html', context)