from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q, Max, Min
from .models import Continent, Country, Indice, Commodity_type, Commodity_profile, President, CentralBank, Bourse, \
    BankRate, MajorExports, UnemploymentRate, GDP, Population
from core.models import CompanyProfile, Indices


class SearchIndexListView(ListView):
    model = Indice
    context_object_name = "indices"
    template_name = "indices_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Indice.objects.filter(
            Q(name__icontains=query) | Q(details__icontains=query)
        )

    def index_count(self):
        return Indice.objects.all().count()


def continent(request, continent_slug):
    continent = get_object_or_404(Continent, slug=continent_slug)
    country = Country.objects.filter(continent=continent).order_by('name')
    paginator = Paginator(country, 50)

    country_count = Country.objects.filter(continent=continent).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'continent': continent,
        'country_count': country_count,
    }
    return render(request, 'continent.html', context)


def country(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    president = President.objects.filter(country=country)
    central_bank = CentralBank.objects.filter(country=country)
    index = Indice.objects.filter(country=country).order_by('name')
    exchange = Bourse.objects.filter(country=country).order_by('name')
    exports = MajorExports.objects.filter(country=country)
    companies = CompanyProfile.objects.filter(country=country).filter(market=1).order_by('?', 'name')[:30]
    bank_rate = BankRate.objects.filter(central_bank=country).order_by('-effective_meeting_date')[:1]
    banks = CompanyProfile.objects.filter(country=country).filter(market=1).filter(industry=6)
    gdp = GDP.objects.filter(country=country)
    population = Population.objects.get(country=country)
    unemployment = UnemploymentRate.objects.filter(country=country)
    paginator = Paginator(index, 50)

    index_count = Indice.objects.filter(country=country).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'country': country,
        'president': president,
        'central_bank': central_bank,
        'index_count': index_count,
        'exchange': exchange,
        'companies': companies,
        'banks': banks,
        'bank_rate': bank_rate,
        'exports': exports,
        'gdp': gdp,
        'unemployment': unemployment,
        'population': population
    }
    return render(request, 'country.html', context)


def index_list(request):
    indices = Indice.objects.all().order_by('country')
    index_count = indices.count()

    context = {
        'indices': indices,
        'index_count': index_count,
    }

    return render(request, 'indices_list.html', context)


def index_summary(request):
    indices = Indice.objects.all().order_by('country')
    index_count = indices.count()

    context = {
        'indices': indices,
        'index_count': index_count,
    }

    return render(request, 'index_summary.html', context)


def index_detail(request, index_id):
    indices = get_object_or_404(Indice, id=index_id)
    companies = CompanyProfile.objects.filter(index=index_id).order_by('name')
    points = Indices.objects.filter(index=index_id)
    point = Indices.objects.filter(index=index_id).last()
    similar_index = Indice.objects.filter(country=1).exclude(name=indices.name).order_by('name')

    index_components = companies.count()

    context = {
        'indices': indices,
        "companies": companies,
        'index_components': index_components,
        'points': points,
        'point': point,
        'ci': Indices.objects.filter(index=index_id).last(),
        'ci_previous': Indices.objects.filter(index=index_id).order_by('-date')[1],
        'similar_index': similar_index,
        'low_52': Indices.objects.filter(index=index_id, date__gt=point.date - timedelta(weeks=52)).order_by('-date')[:14].aggregate(Min("value")),
        'high_52': Indices.objects.filter(index=index_id, date__gt=point.date - timedelta(weeks=52)).order_by('-date')[:14].aggregate(Max("value")),
    }

    return render(request, 'indices_details.html', context)


def commodity_list(request):
    commodities = Commodity_profile.objects.all()
    commodities_count = commodities.count()

    context = {
        'commodities': commodities,
        'commodities_count': commodities_count,
    }
    return render(request, 'commodity.html', context)


def commodity_summary(request):
    commodities = Commodity_profile.objects.all()
    commodities_count = commodities.count()

    context = {
        'commodities': commodities,
        'commodities_count': commodities_count,
    }
    return render(request, 'commodity_summary.html', context)


def commodity_profile(request, commodity_slug):
    commodity_type = get_object_or_404(Commodity_type, slug=commodity_slug)
    commodities = Commodity_profile.objects.filter(category=commodity_type).order_by('name')
    paginator = Paginator(commodities, 50)

    commodities_count = Commodity_profile.objects.filter(category=commodity_type).count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'commodity_type': commodity_type,
        'commodities_count': commodities_count,
    }
    return render(request, 'commodity_profile.html', context)


def commodity_detail(request, commodity_id):
    commodities = get_object_or_404(Commodity_profile, id=commodity_id)

    context = {
        'commodities': commodities
    }

    return render(request, 'commodities_details.html', context)
