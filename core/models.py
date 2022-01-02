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

SHARE_TYPE_CHOICE = (
    ('Private', 'Private'),
    ('Public', 'Public'),
    ('Preference', 'Preference'),
    ('Exchange Tradeable Funds', 'Exchange Tradeable Funds')
)
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
    telephone = models.CharField(max_length=20, blank=True, null=True)
    toll_free = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    core_activities = models.TextField()
    market = models.ManyToManyField(Market, related_name='tags', default='None')
    summary = models.TextField(max_length=2500, blank=True, null=True)
    index = models.ManyToManyField(Indice, blank=True)
    share_type = models.CharField(max_length=255, choices=SHARE_TYPE_CHOICE, default='Public')

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


class ShareDetail(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    issued_shares = models.PositiveBigIntegerField()
    stated_capital = models.PositiveBigIntegerField(blank=True, null=True)
    listed_date = models.DateField()
    financial_period_ends = models.CharField(max_length=255, default="31st December")

    def __str__(self):
        return f"{self.company}"


class SharePrice(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f"{self.company}"


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
    period = models.ManyToManyField(FinancialPeriod)
    file = models.FileField(upload_to='reports')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    audited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company}"


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


class Auditors(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='auditors')
    address = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('auditor', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Registrar(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='auditors', default='sector.png')
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='registrar')
    address = models.CharField(max_length=255)

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
)


class KeyPeople(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='key_pople', default='person.png')
    description = models.TextField()
    birth_date = models.DateField()
    highest_education = models.CharField(max_length=250)
    position = models.CharField(max_length=50, choices=POSITION_CHOICE)
    company = models.ManyToManyField(CompanyProfile, blank=True, related_name='key_people')

    def get_absolute_url(self):
        return reverse('key_people', args=[str(self.id)])

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
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
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


class Opinions(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    docs = models.FileField(upload_to='opinion')
    opinion = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('opinion', args=[str(self.id)])

    def __str__(self):
        return f"{self.author}'s opinion"


