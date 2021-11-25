from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.auth.models import User


user = settings.AUTH_USER_MODEL


class Product(models.Model):
    description = models.TextField()
    brand = models.CharField(max_length=70)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(upload_to='produtos', default='no-image-found.png')

    def get_fullName(self):
        return self.brand + ' ' + self.model

    def __str__(self) -> str:
        return self.get_fullName()


class Client(models.Model):
    name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    address = models.CharField(max_length=200)
    # user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(user, on_delete=models.CASCADE, default=None)

    def get_address(self):
        return self.address

    def get_fullName(self):
        return self.name + ' ' + self.last_name

    def __str__(self) -> str:
        return self.get_fullName()


class Card(models.Model):
    number = models.CharField(null=False, max_length=16)
    valid_date = models.DateField(null=True, blank=True)
    holders_name = models.CharField(max_length=100)
    cvv = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self) -> str:
        line = self.client.get_fullName() + '\'s credit card' + ' id: ' + str(self.id)
        return line


class Demand(models.Model):
    date = models.DateField(null=True, blank=True)
    payment_confirmed = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self) -> str:
        line = 'id: ' + str(self.id) + ' | Product: ' + self.product.get_fullName()
        return line


class Inventory(models.Model):
    amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.product.get_fullName()


class Delivery(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def get_fullAddress(self):
        line = self.client.address + ' - ' + self.district + ' - ' + self.city
        return line

    def get_district(self):
        return self.district

    def get_city(self):
        return self.city
