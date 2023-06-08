from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

from international.models import Country

COUNTRY_CHOICES = (
    ('Ghana', 'Ghana'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, null=True, blank=True)
    # country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, null=True, blank=True)
    country = models.ForeignKey(Country, default=1, null=True, blank=True, on_delete=models.DO_NOTHING)
    birth_date = models.DateField(null=True, blank=True)
    organisation_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
