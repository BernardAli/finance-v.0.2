from django.db import models
from django.urls import reverse

# Create your models here.


class Inflation(models.Model):
    month = models.DateField()
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"Inflation for {self.month} is {self.rate}"


class MPR(models.Model):
    meeting_no = models.PositiveIntegerField(default=1)
    dates = models.CharField(max_length=120)
    effective_date = models.DateField()
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"MPR for {self.dates} is {self.rate}"


SECURITY_CHOICE = (
    ('91 DAY BILL', '91 DAY BILL'),
    ('182 DAY BILL', '182 DAY BILL'),
    ('364 DAY BILL', '364 DAY BILL'),
    ('1 YR FXR BOND', '1 YR FXR BOND'),
    ('2 YR FXR BOND', '2 YR FXR BOND'),
    ('3 YR FXR BOND', '3 YR FXR BOND'),
    ('5 YR FXR BOND', '5 YR FXR BOND'),
    ('6 YR FXR BOND', '6 YR FXR BOND'),
    ('7 YR FXR BOND', '7 YR FXR BOND'),
    ('10 YR FXR BOND', '10 YR FXR BOND'),
    ('15 YR FXR BOND', '15 YR FXR BOND'),
    ('20 YR FXR BOND', '20 YR FXR BOND'),
)


class Security(models.Model):
    security = models.CharField(choices=SECURITY_CHOICE, max_length=50)
    slug = models.SlugField(unique=True, default='91_DAY_BILL')

    def get_absolute_url(self):
        return reverse('t_bills', arg=[self.slug])

    def __str__(self):
        return self.security


class T_BILL(models.Model):
    issue_date = models.DateField()
    tender = models.PositiveIntegerField()
    security = models.ForeignKey(Security, on_delete=models.PROTECT)
    discount = models.DecimalField(max_digits=6, decimal_places=2)
    interest = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.interest}"


PAIR_CHOICE = (
    ('USDGHS', 'USDGHS'),
    ('GBPGHS', 'GBPGHS'),
    ('CHFGHS', 'CHFGHS'),
    ('AUDGHS', 'AUDGHS'),
    ('CADGHS', 'CADGHS'),
    ('DKKGHS', 'DKKGHS'),
    ('JPYGHS', 'JPYGHS'),
    ('NZDGHS', 'NZDGHS'),
    ('NOKGHS', 'NOKGHS'),
    ('SEKGHS', 'SEKGHS'),
    ('ZARGHS', 'ZARGHS'),
    ('EURGHS', 'EURGHS'),
    ('CNYGHS', 'CNYGHS'),
    ('GHSXOF', 'GHSXOF'),
    ('GHSGMD', 'GHSGMD'),
    ('GHSMRO', 'GHSMRO'),
    ('GHSNGN', 'GHSNGN'),
    ('GHSSLL', 'GHSSLL'),
    ('WAUGHS', 'WAUGHS'),
)


class CurrencyPair(models.Model):
    pair = models.CharField(choices=PAIR_CHOICE, max_length=50)
    currency = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, default='usdghs')

    def get_absolute_url(self):
        return reverse('currency', arg=[self.slug])

    def __str__(self):
        return self.pair


class InterbankFX(models.Model):
    date = models.DateField()
    pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    buying = models.DecimalField(max_digits=8, decimal_places=4)
    selling = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return f"{self.pair}"

