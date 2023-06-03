from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from core.models import CompanyProfile
from international.models import Country


# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    picture = models.ImageField(upload_to='news/pictures')
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    companies = models.ManyToManyField(CompanyProfile, related_name='companies', blank=True)
    countries = models.ManyToManyField(Country, related_name='countries', blank=True)
    details = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('news_details', args=[str(self.id)])

    def __str__(self):
        return str(self.title)