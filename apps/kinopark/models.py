from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms


class Movie(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=300, blank=False, default='')
    producer = models.CharField(max_length=50, blank=False, default='')
    rating = models.FloatField(blank=False)
    published = models.BooleanField(default=False)
    image = models.CharField(null=True, max_length=255)

    @property
    def movie_seansy(self):
        return self.seans_set.all()




class Seans(models.Model):
    price = models.BigIntegerField(null=False)
    time = models.TimeField()
    language = models.CharField(max_length=100)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    kinozal_id = models.IntegerField()

    @property
    def seans_seat(self):
        return self.seat_set.all()


class Seat(models.Model):
    seat_number = models.IntegerField()
    available = models.BooleanField()
    seans = models.ForeignKey(Seans, on_delete=models.PROTECT)




class User(AbstractUser):
    first_name = models.CharField(max_length=80, blank=False)
    last_name = models.CharField(max_length=80, blank=False)
    email = models.CharField(max_length=90, blank=False, unique=True)
    username = models.CharField(max_length=90, blank=True, null=True, unique=True)
    password = models.CharField(max_length=90, blank=False)
    # username = None

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Order(models.Model):
    price = models.BigIntegerField(blank=False)
    time = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.PROTECT)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)
