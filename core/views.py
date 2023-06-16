import pandas as pd
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F, Prefetch, Window
from django.db.models.functions import Lag
from django.db.models import Avg, Max, Min, Count
from django.db.models.aggregates import Variance
from django.db.models import Sum, DecimalField, ExpressionWrapper, F, Sum
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q

from django.http import HttpResponse
from django.views.generic import View
from .utils import html_to_pdf

from rates.models import Inflation, MPR, Security, T_BILL, InterbankFX
from .models import Sector, Tag, CompanyProfile, Market, ShareDetail, SharePrice, Indices, Report, \
    MarketReport, PressRelease, Auditors, IPO, Dividend, Ownership, Registrar, Subsidiaries, Opinions, \
    FinancialStatement, Review, FinancialPeriod, ShareSplit, GCX_Types, ShareType, EconomicCalendar, AGM, Advertisement, \
    BankHealth
from news.models import News
from international.models import Continent, Indice, Commodity_type, BankRate, GDP, UnemploymentRate, Commodity_profile
from .utils import average_rating
from .forms import ReviewForm


# Create your views here.


class SearchResultsListView(ListView):
    model = CompanyProfile
    context_object_name = "companies"
    template_name = "companies.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return CompanyProfile.objects.filter(
            Q(name__icontains=query) | Q(core_activities__icontains=query)
        )


def index_view(request):
    inflation = Inflation.objects.last()
    mpr = MPR.objects.last()
    # sectors = CompanyProfile.objects.filter(market__id=1).values('sector__sector').annotate(count=Count('sector')).order_by('-count')
    sectors = CompanyProfile.objects.values('sector__sector').annotate(count=Count('sector')).order_by('-count')
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
    opinions = Opinions.objects.filter(commentary_type='Opinion').order_by('-date')[:3]
    analysis = Opinions.objects.filter(commentary_type='Analysis').order_by('-date')[:3]
    three_months = T_BILL.objects.filter(security=1).last()
    inflation_previous = Inflation.objects.all().order_by('-month')[1]
    mpr_previous = MPR.objects.all().order_by('-effective_date')[1]
    three_months_previous = T_BILL.objects.filter(security=1).order_by('-issue_date')[1]
    dollar_rate = InterbankFX.objects.filter(pair__pair='USDGHS').last()
    dollar_rate_previous = InterbankFX.objects.filter(pair__pair='USDGHS').order_by('-date')[1]
    indices_chart = Indices.objects.filter().order_by('-date')[:2]
    commodities_chart = Commodity_profile.objects.order_by('?')[:2]
    shares_chart = SharePrice.objects.filter().order_by('-date')[:2]
    t_bills_chart = T_BILL.objects.filter().order_by('-tender')[:2]
    share_price_latest = SharePrice.objects.order_by('date').last()
    dividend_calendar = Dividend.objects.filter(qualifying_date__year=2022)
    economic_calendar = EconomicCalendar.objects.filter().order_by('time')
    agm_calendar = AGM.objects.filter().order_by('time')
    today = datetime.today()

    com_numbers = SharePrice.objects.filter(company__market=1).filter(date=share_price_latest.date).count()
    indices_values = Indices.objects.annotate(
        prev_val=Window(
            expression=Lag('value', default=0),
            partition_by=['index'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('value') - F('prev_val')
    ).order_by('-date')[:2]

    t_bills_values = T_BILL.objects.annotate(
        prev_val=Window(
            expression=Lag('interest', default=0),
            partition_by=['security'],
            order_by=F('issue_date').asc(),
        )
    ).annotate(
        diff=F('interest') - F('prev_val')
    ).order_by('-issue_date')[:2]

    sp = SharePrice.objects.filter(company__share_type=1).filter(company__market=1).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', '?')[:2]

    first_index = indices_values.first().index.id
    indices_val = Indices.objects.filter(index=first_index)
    ci_price_first = Indices.objects.filter(index=first_index).order_by('date').first()
    ci_price_latest = Indices.objects.filter(index=first_index).order_by('date').last()

    first_share = sp[0].company.company_id
    share_price = SharePrice.objects.filter(company__company_id=first_share).order_by('-date')
    share_price_first = SharePrice.objects.filter(company__company_id=first_share).order_by('date').first()

    t_bill = T_BILL.objects.filter(security__slug='91_DAY_BILL').order_by('-issue_date')
    t_bill_first = T_BILL.objects.filter(security__slug='91_DAY_BILL').order_by('issue_date').first()
    t_bill_last = T_BILL.objects.filter(security__slug='91_DAY_BILL').order_by('issue_date').last()

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
        'analysis': analysis,
        'three_months': three_months,
        'inflation_previous': inflation_previous,
        'mpr_previous': mpr_previous,
        'three_months_previous': three_months_previous,
        'dollar_rate': dollar_rate,
        'dollar_rate_previous': dollar_rate_previous,
        'indices_chart': indices_chart,
        'commodities_chart': commodities_chart,
        'shares_chart': shares_chart,
        't_bills_chart': t_bills_chart,

        'indices_values': indices_values,
        'sp': sp,
        't_bills_values': t_bills_values,
        'dividend_calendar': dividend_calendar,
        'economic_calendar': economic_calendar,
        'today': today,
        'agm_calendar': agm_calendar,

        'indices_val': indices_val,
        'ci_chart': Indices.objects.filter(index=first_index).order_by('-date')[:5],
        'fsi': Indices.objects.filter(index=first_index).last(),
        'fsi_previous': Indices.objects.filter(index=first_index).order_by('-date')[1],
        'ci_price_first': ci_price_first.date,
        'latest_trading_day': ci_price_latest.date,
        'one_month': ci_price_latest.date - timedelta(weeks=4),
        'six_month': ci_price_latest.date - timedelta(weeks=26),
        'one_year': ci_price_latest.date - timedelta(weeks=52),
        'three_year': ci_price_latest.date - timedelta(weeks=156),
        'five_year': ci_price_latest.date - timedelta(weeks=260),

        'share_price': share_price,
        'share_price_first': share_price_first.date,
        'stock_one_month': share_price_latest.date - timedelta(weeks=4),
        'stock_six_month': share_price_latest.date - timedelta(weeks=26),
        'stock_one_year': share_price_latest.date - timedelta(weeks=52),
        'stock_three_year': share_price_latest.date - timedelta(weeks=156),
        'stock_five_year': share_price_latest.date - timedelta(weeks=260),
        'first_share': first_share,

        't_bill': t_bill,
        't_bill_first': t_bill_first.issue_date,
        't_bill_last': t_bill_last.issue_date,
        't_bill_one_month': t_bill_first.issue_date - timedelta(weeks=4),
        't_bill_six_month': t_bill_first.issue_date - timedelta(weeks=26),
        't_bill_one_year': t_bill_first.issue_date - timedelta(weeks=52),
        't_bill_three_year': t_bill_first.issue_date - timedelta(weeks=156),
        't_bill_five_year': t_bill_first.issue_date - timedelta(weeks=260),
    }

    return render(request, 'index.html', context)


def listed_companies(request):
    companies = CompanyProfile.objects.filter(country=1).order_by('company_id')

    context = {
        'companies': companies
    }
    return render(request, 'companies.html', context)


def company_details(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    industry = company.industry.first().id
    market = company.market.first().id
    similar_company = CompanyProfile.objects.filter(country=company.country).filter(industry__id=industry) \
        .filter(market__id=market).exclude(company_id=company.company_id).order_by('company_id')
    share = ShareDetail.objects.filter(company_id=company_id)
    advert = Advertisement.objects.filter(company_id=company_id).first()
    products = company.products.all().order_by('products')
    brands = company.brands.all().order_by('brand')
    segments = company.segments.all().order_by('segment')
    issued_shares = ShareDetail.objects.filter(company_id=company_id).first()
    share_price = SharePrice.objects.filter(company_id=company_id).order_by('-date')
    country_indices = Indice.objects.filter(country=company.country).order_by('name')
    open_price = SharePrice.objects.filter(company_id=company_id).order_by('date')
    share_price_latest = SharePrice.objects.filter(company_id=company_id).order_by('date').last()
    share_price_first = SharePrice.objects.filter(company_id=company_id).order_by('date').first()
    ipos = IPO.objects.filter(company_id=company_id)
    share_splits = ShareSplit.objects.filter(company_id=company_id)
    auditor = Auditors.objects.filter(company=company_id)
    reports = Report.objects.filter(company_id=company_id)
    reports_qtr = Report.objects.filter(company_id=company_id).filter(period__period='Q1').order_by('-year')
    reports_half = Report.objects.filter(company_id=company_id).filter(period__period='H1').order_by('-year')
    reports_nine = Report.objects.filter(company_id=company_id).filter(period__period='9M').order_by('-year')
    reports_full = Report.objects.filter(company_id=company_id).filter(period__period='FY').order_by('-year')
    dividends = Dividend.objects.filter(company_id=company_id).order_by('-register_closure')
    release = PressRelease.objects.filter(company_id=company_id).order_by('-date')[:5]
    price_year_start = SharePrice.objects.filter(company_id=company_id, date__year=2022).order_by('-date').first()
    price = SharePrice.objects.filter(company_id=company_id).last()
    previous_close = SharePrice.objects.filter(company_id=company_id).order_by('-id')[1]
    ownership = Ownership.objects.filter(company_id=company_id)
    percent_sum = Ownership.objects.aggregate(Sum('percentage_holding'))
    subsidiaries = Subsidiaries.objects.filter(company_id=company_id).all()
    statement = FinancialStatement.objects.filter(company_id=company_id).order_by('file__year').last()
    previous_revenue = FinancialStatement.objects.filter(company_id=company_id).order_by('-file__year').last()
    reviews = company.review_set.all()
    analysis = Opinions.objects.filter(commentary_type='Analysis', company=company).order_by('-date')[:3]
    periods = FinancialPeriod.objects.all()
    # market_cap = price.price * share.issued_shares
    # print(reviews.count())
    company_rating = average_rating([review.rating for review in reviews])
    # df = pd.DataFrame(share_price)
    high_52 = SharePrice.objects.filter(company_id=company_id,
                                        date__gt=share_price_latest.date - timedelta(weeks=52)).order_by(
        'date').aggregate(Max("price"))
    low_52 = SharePrice.objects.filter(company_id=company_id,
                                       date__gt=share_price_latest.date - timedelta(weeks=52)).order_by(
        'date').aggregate(Min("price"))

    statements = FinancialStatement.objects.filter(company_id=company_id).order_by('file__year')

    cap = price.price

    # beta
    indices = Indices.objects.filter(index=1)[:30].aggregate(Variance("value"))
    asset = SharePrice.objects.filter(company_id=company_id).order_by('-date')[:30]
    market = Indices.objects.filter(index=1).order_by('-date')[:30]
    corr = 30
    dividend_latest = Dividend.objects.filter(company_id=company_id).order_by('-register_closure').last()
    bank_health = BankHealth.objects.filter(company_id=company_id).order_by('financial_year')

    sp = SharePrice.objects.filter(company_id=company_id).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        all_time_val=Window(
            expression=Lag('price', 150),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name').all()[:1]
    context = {
        "company_rating": company_rating,
        "reviews": reviews,
        'company': company,
        'share': share,
        'share_price': share_price,
        'country_indices': country_indices,
        'reports': reports,
        'reports_qtr': reports_qtr,
        'reports_half': reports_half,
        'reports_nine': reports_nine,
        'reports_full': reports_full,
        'release': release,
        'auditor': auditor,
        'secretaries': company.secretary.all(),
        'key_people': company.key_people.all().order_by('position'),
        'current_dividend': Dividend.objects.filter(company_id=company_id).order_by('-register_closure')[:1],
        'price': price,
        'ipos': ipos,
        'dividends': dividends,
        'dividend_chart': Dividend.objects.filter(company_id=company_id).order_by('register_closure'),
        'ownership': ownership,
        'similar_company': similar_company,
        # 'market_cap': market_cap,
        "percent_sum": percent_sum,
        'registrars': company.registrar.all(),
        'subsidiaries': subsidiaries,
        'statement': statement,
        'analysis': analysis,
        'previous_close': previous_close,
        'price_year_start': price_year_start,
        'periods': periods,
        'previous_revenue': previous_revenue,
        'share_price_latest': share_price_latest,
        'high_52': high_52,
        'low_52': low_52,
        'one_month': share_price_latest.date - timedelta(weeks=4),
        'six_month': share_price_latest.date - timedelta(weeks=26),
        'one_year': share_price_latest.date - timedelta(weeks=52),
        'share_price_first': share_price_first.date,
        'open_price': open_price,
        # 'price_book': df.to_html(),
        'ma5': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:5].aggregate(Avg("price")),
        'ma10': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:10].aggregate(Avg("price")),
        'ma20': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:20].aggregate(Avg("price")),
        'ma50': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:50].aggregate(Avg("price")),
        'ma100': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:100].aggregate(Avg("price")),
        'low_14': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:14].aggregate(Min("price")),
        'high_14': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:14].aggregate(Max("price")),

        'statements': statements,
        'cap': cap * issued_shares.issued_shares if issued_shares else 0,
        'indices': indices,
        'corr': corr,
        'dividend_latest': dividend_latest,
        'advert': advert,
        'products': products,
        'brands': brands,
        'segments': segments,
        'share_splits': share_splits,
        'sp': sp,
        'bank_health': bank_health
    }
    return render(request, 'company_details.html', context)


def company_file(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    industry = company.industry.first().id
    market = company.market.first().id
    similar_company = CompanyProfile.objects.filter(country=company.country).filter(industry__id=industry) \
        .filter(market__id=market).exclude(company_id=company.company_id).order_by('company_id')
    share = ShareDetail.objects.filter(company_id=company_id)
    products = company.products.all().order_by('products')
    issued_shares = ShareDetail.objects.filter(company_id=company_id).first()
    open_price = SharePrice.objects.filter(company_id=company_id).order_by('date')
    share_price_latest = SharePrice.objects.filter(company_id=company_id).order_by('date').last()
    share_price = SharePrice.objects.filter(company_id=company_id).filter(
        date__gt=share_price_latest.date - timedelta(weeks=4)).order_by('-date')
    share_price_first = SharePrice.objects.filter(company_id=company_id).order_by('date').first()
    ipos = IPO.objects.filter(company_id=company_id)
    share_splits = ShareSplit.objects.filter(company_id=company_id)
    country_indices = Indice.objects.filter(country=company.country).order_by('name')
    auditor = Auditors.objects.filter(company=company_id)
    reports = Report.objects.filter(company_id=company_id)
    reports_qtr = Report.objects.filter(company_id=company_id).filter(period__period='Q1')
    reports_half = Report.objects.filter(company_id=company_id).filter(period__period='H1')
    reports_nine = Report.objects.filter(company_id=company_id).filter(period__period='9M')
    reports_full = Report.objects.filter(company_id=company_id).filter(period__period='FY')
    dividends = Dividend.objects.filter(company_id=company_id).order_by('-register_closure')[:1]
    release = PressRelease.objects.filter(company_id=company_id).order_by('-date')[:5]
    price_year_start = SharePrice.objects.filter(company_id=company_id, date__year=2022).order_by('-date').first()
    price = SharePrice.objects.filter(company_id=company_id).last()
    previous_close = SharePrice.objects.filter(company_id=company_id).order_by('-id')[1]
    ownership = Ownership.objects.filter(company_id=company_id)
    percent_sum = Ownership.objects.aggregate(Sum('percentage_holding'))
    subsidiaries = Subsidiaries.objects.filter(company_id=company_id).all()
    statement = FinancialStatement.objects.filter(company_id=company_id).order_by('file__year').last()
    previous_revenue = FinancialStatement.objects.filter(company_id=company_id).order_by('-file__year')[1]
    reviews = company.review_set.all()
    analysis = Opinions.objects.filter(commentary_type='Analysis', company=company).order_by('-date')[:3]
    periods = FinancialPeriod.objects.all()
    # market_cap = price.price * share.issued_shares
    print(reviews.count())
    company_rating = average_rating([review.rating for review in reviews])
    # df = pd.DataFrame(share_price)
    high_52 = SharePrice.objects.filter(company_id=company_id,
                                        date__gt=share_price_latest.date - timedelta(weeks=52)).order_by(
        'date').aggregate(Max("price"))
    low_52 = SharePrice.objects.filter(company_id=company_id,
                                       date__gt=share_price_latest.date - timedelta(weeks=52)).order_by(
        'date').aggregate(Min("price"))

    statements = FinancialStatement.objects.filter(company_id=company_id).order_by('file__year')

    cap = price.price

    # beta
    indices = Indices.objects.filter(index=1)[:30].aggregate(Variance("value"))
    asset = SharePrice.objects.filter(company_id=company_id).order_by('-date')[:30]
    market = Indices.objects.filter(index=1).order_by('-date')[:30]
    corr = 30
    dividend_latest = Dividend.objects.filter(company_id=company_id).order_by('-register_closure').last()

    context = {
        "company_rating": company_rating,
        "reviews": reviews,
        'company': company,
        'share': share,
        'share_price': share_price,
        'country_indices': country_indices,
        'reports': reports,
        'reports_qtr': reports_qtr,
        'reports_half': reports_half,
        'reports_nine': reports_nine,
        'reports_full': reports_full,
        'release': release,
        'auditor': auditor,
        'secretaries': company.secretary.all(),
        'key_people': company.key_people.all(),
        'price': price,
        'ipos': ipos,
        'dividends': dividends,
        'ownership': ownership,
        'similar_company': similar_company,
        # 'market_cap': market_cap,
        "percent_sum": percent_sum,
        'registrars': company.registrar.all(),
        'subsidiaries': subsidiaries,
        'statement': statement,
        'analysis': analysis,
        'previous_close': previous_close,
        'price_year_start': price_year_start,
        'periods': periods,
        'previous_revenue': previous_revenue,
        'share_price_latest': share_price_latest,
        'high_52': high_52,
        'low_52': low_52,
        'one_month': share_price_latest.date - timedelta(weeks=4),
        'six_month': share_price_latest.date - timedelta(weeks=26),
        'one_year': share_price_latest.date - timedelta(weeks=52),
        'share_price_first': share_price_first.date,
        'open_price': open_price,
        # 'price_book': df.to_html(),
        'ma5': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:5].aggregate(Avg("price")),
        'ma10': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:10].aggregate(Avg("price")),
        'ma20': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:20].aggregate(Avg("price")),
        'ma50': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:50].aggregate(Avg("price")),
        'ma100': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:100].aggregate(Avg("price")),
        'low_14': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:14].aggregate(Min("price")),
        'high_14': SharePrice.objects.filter(company_id=company_id).order_by('-date')[:14].aggregate(Max("price")),

        'statements': statements,
        'cap': cap * issued_shares.issued_shares,

        'indices': indices,
        'corr': corr,
        'dividend_latest': dividend_latest,
        'products': products,
        'share_splits': share_splits
    }
    open('templates/temp.html', "w").write(render_to_string('company_details_file.html', context))

    # Converting the HTML template into a PDF file
    pdf = html_to_pdf('temp.html')

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, 'temp.html', context)


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


def opinions_details(request, opinions_id):
    opinions = get_object_or_404(Opinions, id=opinions_id)

    context = {
        'opinions': opinions,
    }

    return render(request, 'opinions_details.html', context)


def sector(request, sector_slug):
    sector = get_object_or_404(Sector, slug=sector_slug)
    companies = CompanyProfile.objects.filter(sector=sector, country=1).order_by('name')
    paginator = Paginator(companies, 50)

    sector_count = companies.count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sector': sector,
        'sector_count': sector_count,
    }
    return render(request, 'sectors.html', context)


def market_detail(request, market_slug):
    market = get_object_or_404(Market, slug=market_slug)
    companies = CompanyProfile.objects.filter(market=market).order_by('name')
    market_count = CompanyProfile.objects.filter(market=market).count()
    share_price_latest = SharePrice.objects.order_by('date').last()

    share_price = SharePrice.objects.filter(date=share_price_latest.date)
    share_detail = ShareDetail.objects.select_related('company')
    data = CompanyProfile.objects.filter(share_type=1).filter(market=market).prefetch_related(
        Prefetch("share_price", queryset=share_price),
        Prefetch("statement", queryset=FinancialStatement.objects.all()),
        Prefetch("dividend", queryset=Dividend.objects.all()),
        Prefetch("share_details", queryset=share_detail)).order_by('name')

    com_numbers = SharePrice.objects.filter(company__market=market).filter(date=share_price_latest.date).count()
    sp = SharePrice.objects.filter(company__market=market).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:com_numbers]

    context = {
        'market': market,
        'companies': companies,
        'market_count': market_count,
        'sp': sp,
        'data': data

    }
    return render(request, 'market_detail.html', context)


def share_type_detail(request, share_type_id):
    share = get_object_or_404(ShareType, id=share_type_id)
    share_type_count = CompanyProfile.objects.filter(share_type=share.id).count()

    share_price_latest = SharePrice.objects.order_by('date').last()
    share_price = SharePrice.objects.filter(date=share_price_latest.date)
    share_detail = ShareDetail.objects.select_related('company')
    data = CompanyProfile.objects.filter(share_type=share.id).prefetch_related(
        Prefetch("share_price", queryset=share_price),
        Prefetch("statement", queryset=FinancialStatement.objects.all()),
        Prefetch("dividend", queryset=Dividend.objects.all()),
        Prefetch("share_details", queryset=share_detail)).order_by('name')

    sp = SharePrice.objects.filter(company__share_type=share.id).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:share_type_count]

    context = {
        'share': share,
        'sp': sp,
        'data': data,
        'share_type_count': share_type_count,

    }
    return render(request, 'share_type_details.html', context)


def share_type_detail_perfomance(request, share_type_id):
    share = get_object_or_404(ShareType, id=share_type_id)
    companies = CompanyProfile.objects.filter(share_type=share.id).order_by('share_type')
    share_type_count = CompanyProfile.objects.filter(share_type=share.id).count()
    share_price_latest = SharePrice.objects.order_by('date').last()

    share_price = SharePrice.objects.filter(date=share_price_latest.date)
    share_detail = ShareDetail.objects.select_related('company')
    data = CompanyProfile.objects.filter(share_type=share.id).prefetch_related(
        Prefetch("share_price", queryset=share_price),
        Prefetch("statement", queryset=FinancialStatement.objects.all()),
        Prefetch("dividend", queryset=Dividend.objects.all()),
        Prefetch("share_details", queryset=share_detail)).order_by('name')

    com_numbers = SharePrice.objects.filter(company__share_type=share).filter(date=share_price_latest.date).count()
    sp = SharePrice.objects.filter(company__share_type=share).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:com_numbers]

    context = {
        'share': share,
        'companies': companies,
        'share_type_count': share_type_count,
        'sp': sp,
        'data': data

    }
    return render(request, 'share_type_detail_perfomance.html', context)


def stock_market_view(request):
    sectors = Sector.objects.all()
    markets = Market.objects.exclude(market='None')
    shares_types = ShareType.objects.all()
    indices = Indices.objects.filter(index__symbol='GSE-CI')
    fsi_indices = Indices.objects.filter(index__symbol='GSE-FSI')
    auditors = Auditors.objects.all().order_by('name')[:8]
    registrars = Registrar.objects.all().order_by('name')[:8]
    market_reports = MarketReport.objects.all().order_by('-session_number')[:5]
    share_price_latest = SharePrice.objects.order_by('-date').first()

    companies = CompanyProfile.objects.filter(country=1).filter(market=1).order_by('name')
    companies_counts = CompanyProfile.objects.filter(country=1).count()
    ci_price_first = Indices.objects.filter(index__symbol='GSE-CI').order_by('date').first()
    ci_price_latest = Indices.objects.filter(index__symbol='GSE-CI').order_by('date').last()

    fsi_price_first = Indices.objects.filter(index__symbol='GSE-CI').order_by('date').first()
    fsi_price_latest = Indices.objects.filter(index__symbol='GSE-CI').order_by('date').last()

    stock_performance = SharePrice.objects.filter(date__gt='2022-12-31').values('company__name', 'company__company_id').\
        annotate(total_price=Sum('price')).annotate(total_volume=Sum('volume')).annotate(total_trasaction_value=Sum(F('price') * F('volume'))).order_by('-total_trasaction_value')

    com_numbers = SharePrice.objects.filter(company__share_type=1).filter(date=share_price_latest.date).count()
    indices_values = Indices.objects.annotate(
        prev_val=Window(
            expression=Lag('value', default=0),
            partition_by=['index'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('value', 50),
            partition_by=['index'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('value') - F('prev_val')
    ).order_by('-date')[:2]
    sp = SharePrice.objects.filter(company__share_type=1).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:com_numbers]

    context = {
        'sectors': sectors,
        'markets': markets,
        'shares_types': shares_types,
        'indices': indices,
        'fsi_indices': fsi_indices,
        'market_reports': market_reports,
        'companies': companies,
        'auditors': auditors,
        'registrars': registrars,
        'companies_counts': companies_counts,

        'sp': sp,
        'indices_values': indices_values,

        'ci': Indices.objects.filter(index__symbol='GSE-CI').last(),
        'ci_previous': Indices.objects.filter(index__symbol='GSE-CI').order_by('-date')[1],
        'ci_chart': Indices.objects.filter(index__symbol='GSE-CI').order_by('-date')[:5],
        'fsi': Indices.objects.filter(index__symbol='GSE-FSI').last(),
        'fsi_previous': Indices.objects.filter(index__symbol='GSE-FSI').order_by('-date')[1],
        'share_price_first': ci_price_first.date,
        'share_price_latest': ci_price_latest,
        'one_month': ci_price_latest.date - timedelta(weeks=4),
        'six_month': ci_price_latest.date - timedelta(weeks=26),
        'one_year': ci_price_latest.date - timedelta(weeks=52),
        'three_year': ci_price_latest.date - timedelta(weeks=156),
        'five_year': ci_price_latest.date - timedelta(weeks=260),

        'fsi_share_price_first': ci_price_first.date,
        'fsi_share_price_latest': ci_price_latest,
        'fsi_one_month': ci_price_latest.date - timedelta(weeks=4),
        'fsi_six_month': ci_price_latest.date - timedelta(weeks=26),
        'fsi_one_year': ci_price_latest.date - timedelta(weeks=52),
        'fsi_three_year': ci_price_latest.date - timedelta(weeks=156),
        'fsi_five_year': ci_price_latest.date - timedelta(weeks=260),

        'stock_performance': stock_performance
    }

    return render(request, 'stock_market.html', context)


def industry_view(request, tag_slug):
    industry = get_object_or_404(Tag, slug=tag_slug)
    companies = CompanyProfile.objects.filter(industry=industry).order_by('company_id')
    industry_alt = Tag.objects.exclude(slug=tag_slug).order_by('slug')

    paginator = Paginator(companies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    industry_count = CompanyProfile.objects.filter(industry=industry).count()
    share_price_latest = SharePrice.objects.filter(company__industry=industry).order_by('-date').first()
    share_price = SharePrice.objects.filter(date=share_price_latest.date)
    share_detail = ShareDetail.objects.select_related('company')
    # data = CompanyProfile.objects.filter(share_type=1).prefetch_related("share_details", "share_price")
    data = CompanyProfile.objects.filter(industry=industry).prefetch_related(
        Prefetch("share_price", queryset=share_price),
        Prefetch("statement", queryset=FinancialStatement.objects.all()),
        Prefetch("dividend", queryset=Dividend.objects.all()),
        Prefetch("share_details", queryset=share_detail)).order_by('name')
    total_volume = SharePrice.objects.filter(date=share_price_latest.date).aggregate(Sum('volume'))

    # Test
    com_numbers = SharePrice.objects.filter(company__industry=industry).filter(date=share_price_latest.date).count()
    sp = SharePrice.objects.filter(company__industry=industry).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:com_numbers]

    context = {
        'page_obj': page_obj,
        'industry': industry,
        'industry_count': industry_count,
        'data': data,
        'sp': sp,
        'industry_alt': industry_alt
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

    latest_date = SharePrice.objects.order_by('-date').first().date

    sp = SharePrice.objects.filter(company__market=market).order_by('company__name').annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).order_by('-date', 'company__name')[:market_count]

    context = {
        'page_obj': page_obj,
        'market': market,
        'market_count': market_count,
        'sp': sp,
        'latest_date': latest_date
    }
    return render(request, 'market.html', context)


def company_summary(request):
    share_price_latest = SharePrice.objects.order_by('-date').first()
    companies = SharePrice.objects.filter(date=share_price_latest.date).select_related('company').count()
    share_price_previous = SharePrice.objects.order_by('-date')[companies]
    share_price = SharePrice.objects.filter(date=share_price_latest.date)
    share_price2 = SharePrice.objects.filter(date=share_price_previous.date)
    share_detail = ShareDetail.objects.select_related('company')
    # data = CompanyProfile.objects.filter(share_type=1).prefetch_related("share_details", "share_price")
    data = CompanyProfile.objects.exclude(market=3).prefetch_related(
        Prefetch("share_price", queryset=share_price),
        Prefetch("statement", queryset=FinancialStatement.objects.all()),
        Prefetch("dividend", queryset=Dividend.objects.all()),
        Prefetch("share_details", queryset=share_detail)).order_by('name')
    total_volume = SharePrice.objects.filter(date=share_price_latest.date).aggregate(Sum('volume'))

    # Test
    com_numbers = SharePrice.objects.filter(company__share_type=1).filter(date=share_price_latest.date).count()
    sp = SharePrice.objects.filter(company__share_type=1).annotate(
        prev_val=Window(
            expression=Lag('price', default=0),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_wk_val=Window(
            expression=Lag('price', default=5),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        prev_mothn_val=Window(
            expression=Lag('price', 20),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        ytd_val=Window(
            expression=Lag('price', 50),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        one_yr_val=Window(
            expression=Lag('price', 262),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        three_yr_val=Window(
            expression=Lag('price', 786),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        five_yr_val=Window(
            expression=Lag('price', 1310),
            partition_by=['company'],
            order_by=F('date').asc(),
        )
    ).annotate(
        diff=F('price') - F('prev_val')
    ).annotate(
        year_diff=F('price') - F('ytd_val')
    ).order_by('-date', 'company__name')[:com_numbers]

    # days calculation
    one_month = share_price_latest.date - timedelta(weeks=12)
    three_months = share_price_latest.date - timedelta(weeks=12)
    three_months_volume = SharePrice.objects.filter(date__lt=three_months).aggregate(Sum('volume'))
    three_months_days = SharePrice.objects.filter(date__lt=three_months).count()
    context = {
        'companies': companies,
        'share_price_latest': share_price_latest,
        'share_price': share_price,
        'data': data,
        'total_volume': total_volume,
        'gse_ci_one_month': Indices.objects.filter(index=1).filter(date__lt=one_month).last(),
        'gse_ci_open': Indices.objects.filter(index=1).last(),
        'gse_ci_previous_close': Indices.objects.filter(index=1).order_by('-date')[1],
        'gse_ci_year_start': Indices.objects.filter(index=1).filter(date__gt='2023-01-01').first(),
        'three_months_volume': three_months_volume,
        'three_months_days': three_months_days,
        'share_price2': share_price2,
        'sp': sp
    }
    return render(request, 'trading_summary.html', context)


def auditor_detail(request, auditor_id):
    auditor = get_object_or_404(Auditors, id=auditor_id)
    companies = auditor.company.all().order_by('name')
    services = auditor.services.all().order_by('services')

    context = {
        'auditor': auditor,
        'companies': companies,
        'services': services
    }

    return render(request, 'auditor_details.html', context)


def registrar_detail(request, registrar_id):
    registrar = get_object_or_404(Registrar, id=registrar_id)
    companies = registrar.company.all().order_by('name')

    context = {
        'registrar': registrar,
        'companies': companies
    }

    return render(request, 'registrar_details.html', context)


def review_edit(request, company_pk, review_pk=None):
    company = get_object_or_404(CompanyProfile, id=company_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, company_id=company_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.company = company

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(company))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(company))

            updated_review.save()
            return redirect("company_details", company.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "publisher_edit.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": company,
                   "related_model_type": "CompanyProfile"
                   })


def gcx_home(request):
    comm_types = GCX_Types.objects.all()
    context = {
        'comm_types': comm_types
    }
    return render(request, "gcx_home.html", context)


def economic_calendar(request):
    dividend_calendar = Dividend.objects.filter()
    economic_calendar = EconomicCalendar.objects.filter().order_by('time')
    agm_calendar = AGM.objects.filter().order_by('time')
    context = {
        'dividend_calendar': dividend_calendar,
        'economic_calendar': economic_calendar,
        'agm_calendar': agm_calendar
    }
    return render(request, "economic_calendar.html", context)
