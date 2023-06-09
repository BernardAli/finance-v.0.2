from django.db import models
from django.urls import reverse


# Create your models here.

class Topics(models.Model):
    topic = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to='topic', default='sector.png')
    slug = models.SlugField(unique=True, default='financial')

    def get_absolute_url(self):
        return reverse('topic_details', args=[self.slug])

    def __str__(self):
        return self.topic


class FirstAlphabet(models.Model):
    alphabet = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to='topic', default='sector.png')
    slug = models.SlugField(unique=True, default='A')

    def get_absolute_url(self):
        return reverse('sector', arg=[self.slug])

    def __str__(self):
        return self.alphabet


class Term(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.DO_NOTHING, related_name='term')
    first_letter = models.ForeignKey(FirstAlphabet, on_delete=models.DO_NOTHING, related_name='first_letter')
    word = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to='term', default='sector.png')
    take_away = models.CharField(max_length=255, unique=True)
    meaning = models.TextField(unique=True)
    example = models.TextField(unique=True)
    video_url = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse('term_details', args=[str(self.id)])

    def __str__(self):
        return self.word