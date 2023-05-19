from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

CONTINENT_CHOICE = (
    ('Africa', 'Africa'),
    ('Europe', 'Europe'),
    ('Middle East', 'Middle East'),
    ('Asia', 'Asia'),
    ('Americas', 'Americas'),
    ('Oceania', 'Oceania')
)


class Continent(models.Model):
    continent = models.CharField(choices=CONTINENT_CHOICE, max_length=50)
    slug = models.SlugField(unique=True, default='Europe')
    icon = models.ImageField(upload_to='continent', default='globe.svg')

    def get_absolute_url(self):
        return reverse('continent', arg=[self.slug])

    def __str__(self):
        return self.continent


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)
    slug = models.SlugField(unique=True, blank=True, null=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    flag = models.ImageField(upload_to='country', default='globe.svg')
    currency = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=3)
    dialing_code = models.CharField(max_length=25, default='+233')
    area_size = models.PositiveIntegerField(default=30)
    time_zone = models.CharField(max_length=25, default='GMT+0')
    capital = models.CharField(max_length=255, default='Accra')

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('country', arg=[self.slug])

    def __str__(self):
        return self.name


active_choices = (
    ('Active', 'Active'),
    ('Former', 'Former'),
)


class President(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='presidents', default='sector.png')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    url = models.CharField(max_length=255)
    elected_date = models.DateField()
    active = models.CharField(max_length=10, default='Active', choices=active_choices)

    def get_absolute_url(self):
        return reverse('president', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Bourse(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    commenced_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='bourse', default='sector.png')
    about = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('bourse', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Indice(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    main_exchange = models.ForeignKey(Bourse, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('index_detail', args=[str(self.id)])

    def __str__(self):
        return self.symbol


COMMODITY_TYPE_CHOICE = (
    ('Precious Metals', 'Precious Metals'),
    ('Base Metals', 'Base Metals'),
    ('Energies', 'Energies'),
    ('Soft Commodities', 'Soft Commodities'),
)


class Commodity_type(models.Model):
    commodity_type = models.CharField(choices=COMMODITY_TYPE_CHOICE, max_length=255)
    slug = models.SlugField(unique=True, default='soft')
    icon = models.ImageField(upload_to='commodity_type', default='commodities.png')

    def get_absolute_url(self):
        return reverse('commodity_type', arg=[self.slug])

    def __str__(self):
        return self.commodity_type


class Commodity_profile(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    category = models.ForeignKey(Commodity_type, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default='soft')
    icon = models.ImageField(upload_to='commodity_type', default='commodities.png')
    exchange = models.CharField(max_length=255)
    contract_size = models.CharField(max_length=255)
    point_size = models.CharField(max_length=900)

    def get_absolute_url(self):
        return reverse('commodity_detail', arg=[self.slug])

    def __str__(self):
        return self.name


class CentralBank(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='central_banks', default='sector.png')
    country = models.ManyToManyField(Country, related_name='central_bank')
    url = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('central_bank', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class BankRate(models.Model):
    central_bank = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='central_bank_rate')
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    effective_meeting_date = models.DateField()
    next_meeting_date = models.DateField()
    realeased_file = models.FileField(upload_to='base_rate', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('central_bank_rate', args=[str(self.id)])

    def __str__(self):
        return f"{self.central_bank} {self.rate}"


export_choices = (
    ('Base Metals', 'Base Metals'),
    ('Crude', 'Crude'),
    ('Cocoa', 'Cocoa'),
    ('Coal', 'Coal'),
    ('Banana', 'Banana'),
    ('Machinery', 'Machinery'),
    ('Machinery', 'Machinery'),
)


class MajorExports(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    export = models.ManyToManyField(Commodity_profile)

    def get_absolute_url(self):
        return reverse('export', args=[str(self.id)])

    def __str__(self):
        return f"{self.country} {self.export}"


class UnemploymentRate(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='unemployment')
    date = models.DateField(default='2020-12-31')
    value = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('unemployment', args=[str(self.id)])

    def __str__(self):
        return f"{self.country} {self.value}"


class GDP(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='gdp')
    date = models.DateField(default='2020-12-31')
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = '-value',

    def get_absolute_url(self):
        return reverse('gdp', args=[str(self.id)])

    def __str__(self):
        return f"{self.country} {self.value}"
