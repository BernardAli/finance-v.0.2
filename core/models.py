from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
from django.conf import settings
from international.models import Indice, Country


# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('industry', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Sector(models.Model):
    sector = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='sector', default='sector.png')
    slug = models.SlugField(unique=True, default='financial')

    def get_absolute_url(self):
        return reverse('sector', arg=[self.slug])

    def __str__(self):
        return self.sector


class Market(models.Model):
    market = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='sector', default='sector.png')
    slug = models.SlugField(unique=True, default='GSE')

    def get_absolute_url(self):
        return reverse('market', arg=[self.slug])

    def __str__(self):
        return self.market


class Products(models.Model):
    products = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('products', args=[str(self.id)])

    def __str__(self):
        return f"{self.products}"


class Brand(models.Model):
    brand = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand}"


class OperatingSegment(models.Model):
    segment = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.segment}"


SHARE_TYPE_CHOICE = (
    ('Equity', 'Equity'),
    ('Preference', 'Preference'),
    ('Depository Shares', 'Depository Shares'),
    ('Exchange Tradeable Funds', 'Exchange Tradeable Funds'),
)


class ShareType(models.Model):
    share_type = models.CharField(max_length=255, choices=SHARE_TYPE_CHOICE, default='Equity')

    def get_absolute_url(self):
        return reverse('share_type_details', arg=[self.slug])

    def __str__(self):
        return self.share_type


class CompanyProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='company', default='sector.png')
    isin = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sector = models.ManyToManyField(Sector, related_name='tags', blank=True)
    industry = models.ManyToManyField(Tag, related_name='tags', blank=True)
    postal_address = models.CharField(max_length=255, blank=True, null=True)
    registered_office = models.CharField(max_length=255, blank=True, null=True)
    incorporated_date = models.DateField(blank=True, null=True)
    employees = models.IntegerField(default=0)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    toll_free = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    core_activities = models.TextField()
    products = models.ManyToManyField(Products, blank=True)
    brands = models.ManyToManyField(Brand, blank=True)
    segments = models.ManyToManyField(OperatingSegment, blank=True)
    market = models.ManyToManyField(Market, related_name='tags', default='None')
    summary = models.TextField(max_length=2500, blank=True, null=True)
    index = models.ManyToManyField(Indice, blank=True)
    share_type = models.ManyToManyField(ShareType, related_name='tags', blank=True, default=1)

    def get_absolute_url(self):
        return reverse('company_details', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 600, 800

        if self.logo:
            pic = Image.open(self.logo.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.logo.path)

    def __str__(self):
        return str(self.company_id)


class Subsidiaries(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    subsidiary_name = models.CharField(max_length=255)
    ownership_pct = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.subsidiary_name}"


class ShareSplit(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='share_splits')
    old_fv = models.DecimalField(max_digits=5, decimal_places=2)
    new_fv = models.DecimalField(max_digits=5, decimal_places=2)
    split_date = models.DateField()

    def __str__(self):
        return f"{self.company}"


class Advertisement(models.Model):
    url = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='adverts')

    def __str__(self):
        return f"{self.url}"


STATUS_CHOICE = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)


class ShareDetail(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='share_details')
    issued_shares = models.PositiveBigIntegerField()
    stated_capital = models.PositiveBigIntegerField(blank=True, null=True)
    listed_date = models.DateField()
    financial_period_ends = models.CharField(max_length=255, default="31st December")
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="Active")

    def __str__(self):
        return f"{self.company}"


class SharePrice(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='share_price')
    date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f"{self.company}, {self.price}"


class Indices(models.Model):
    index = models.ForeignKey(Indice, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.index}"


PERIOD_CHOICE = (
    ('Q1', '1st Quarter'),
    ('H1', '1st Half'),
    ('9M', '9 Months'),
    ('FY', 'Full Year'),
)


class FinancialPeriod(models.Model):
    period = models.CharField(max_length=50, choices=PERIOD_CHOICE)
    slug = models.SlugField(unique=True, default='fy')

    def get_absolute_url(self):
        return reverse('period', arg=[self.slug])

    def __str__(self):
        return f"{self.period}"


class Report(models.Model):
    year = models.DateField()
    period = models.ForeignKey(FinancialPeriod, on_delete=models.CASCADE)
    file = models.FileField(upload_to='reports')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    audited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} - {self.year}"


class BankHealth(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    financial_year = models.IntegerField(default='2022')
    total_deposits = models.BigIntegerField()
    netAdvances = models.BigIntegerField()
    netImpairments = models.BigIntegerField()

    def __str__(self):
        return f"{self.financial_year}"


class MarketReport(models.Model):
    date = models.DateField(unique=True)
    file = models.FileField(upload_to='reports')
    session_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.session_number}"


class PressRelease(models.Model):
    file = models.FileField(upload_to='reports')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.company}"


class AuditingServices(models.Model):
    services = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('auditing_services', args=[str(self.id)])

    def __str__(self):
        return f"{self.services}"


class Auditors(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='auditors')
    address = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    incorporated_date = models.DateField(blank=True, null=True)
    services = models.ManyToManyField(AuditingServices, blank=True)

    def get_absolute_url(self):
        return reverse('auditor', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Registrar(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='registrar')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    business_nature = models.TextField(blank=True, null=True)
    incorporated_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('registrar', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Secretary(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='secretary')
    slug = models.SlugField(unique=True, default='None')
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Solicitor(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='solicitor')
    slug = models.SlugField(unique=True, default='None')
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


POSITION_CHOICE = (
    ('CEO', 'CEO'),
    ('Chairman', 'Chairman'),
    ('Director', 'Director'),
    ('C.F.O', 'C.F.O'),
    ('Member', 'Member'),
)


class KeyPeople(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='key_pople', default='person.png')
    description = models.TextField()
    birth_date = models.DateField()
    highest_education = models.CharField(max_length=250)
    position = models.CharField(max_length=50, choices=POSITION_CHOICE)
    appointment_date = models.DateField(null=True, blank=True)
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='key_people')

    def get_absolute_url(self):
        return reverse('key_people', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


MANAGEMENT_POSITION_CHOICE = (
    ('CEO', 'CEO'),
    ('C.F.O', 'C.F.O'),
    ('C.H.R', 'C.H.R'),
    ('HEAD OF SALES AND MARKETING', 'HEAD OF SALES AND MARKETING'),
    ('HEAD OF QUALITY AND REGULATORY AFFAIRS', 'HEAD OF QUALITY AND REGULATORY AFFAIRS'),
    ('HEAD OF SUPPLY CHAIN', 'HEAD OF SUPPLY CHAIN'),
)


class Management(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='key_pople', default='person.png')
    description = models.TextField()
    birth_date = models.DateField()
    highest_education = models.CharField(max_length=250)
    position = models.CharField(max_length=50, choices=MANAGEMENT_POSITION_CHOICE)
    appointment_date = models.DateField(null=True, blank=True)
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='management')

    def get_absolute_url(self):
        return reverse('management', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class IPO(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='ipo')
    prospectus = models.FileField(upload_to='prospectus')
    ipo_date = models.DateField()
    ipo_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.company}"


class Dividend(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="dividend")
    financial_year = models.IntegerField(default='2020')
    file = models.FileField(upload_to='dividends')
    final_dividend = models.DecimalField(max_digits=7, decimal_places=4)
    qualifying_date = models.DateField()
    register_closure = models.DateField()
    ex_dividend_date = models.DateField()
    payment_date = models.DateField()
    agm = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('dividend', args=[str(self.id)])

    def __str__(self):
        return f"{self.company}'s dividend"


class Ownership(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    date = models.DateField()
    shareholder_name = models.CharField(max_length=255)
    shares_owned = models.PositiveBigIntegerField()
    percentage_holding = models.DecimalField(max_digits=4, decimal_places=2)

    def get_absolute_url(self):
        return reverse('ownership', args=[str(self.id)])

    def __str__(self):
        return f"{self.company}'s ownership"


TYPE_CHOICE = (
    ('Opinion', 'Opinion'),
    ('Analysis', 'Analysis'),
)


class Opinions(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    commentary_type = models.CharField(max_length=10, choices=TYPE_CHOICE, default='Analysis')
    title = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    docs = models.FileField(upload_to='opinion')
    opinion = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('opinions_details', args=[str(self.id)])

    def __str__(self):
        return f"{self.author}'s opinion"


class FinancialStatement(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="statement")
    auditor = models.ForeignKey(Auditors, on_delete=models.PROTECT, null=True, blank=True)
    financial_period = models.ForeignKey(FinancialPeriod, on_delete=models.PROTECT)
    file = models.ForeignKey(Report, on_delete=models.PROTECT)
    net_sales_revenue = models.BigIntegerField()
    total_operating_revenue = models.BigIntegerField()
    operating_profit_ebit = models.BigIntegerField()
    gross_profit_ebitda = models.BigIntegerField()
    net_profit_loss = models.BigIntegerField()
    total_asset = models.BigIntegerField()
    total_equity = models.BigIntegerField()
    current_asset = models.BigIntegerField()
    total_cash = models.BigIntegerField()
    inventory = models.BigIntegerField()
    current_liability = models.BigIntegerField()
    total_liability = models.BigIntegerField()
    operating_cash_flow = models.BigIntegerField()
    investing_cash_flow = models.BigIntegerField()
    financing_cash_flow = models.BigIntegerField()

    def __str__(self):
        return f'{self.company} - {self.financial_period} Financial Statement'


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(auto_now=True,
                                       help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                help_text="The Company that this review is for.")

    def __str__(self):
        return f'{self.creator.username} - {self.company.name}'


class GCX_Types(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='commodies', default='sector.png')

    def __str__(self):
        return f'{self.name}'


class EconomicCalendar(models.Model):
    time = models.DateTimeField()
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    event = models.CharField(max_length=255)
    actual = models.IntegerField()
    forecast = models.IntegerField()
    previous = models.IntegerField()
    file = models.FileField(upload_to='calendar')

    def __str__(self):
        return f'{self.event}'


class AGM(models.Model):
    date = models.DateField()
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    time = models.TimeField()
    venue = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.company}'
