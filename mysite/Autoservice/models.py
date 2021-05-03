from django.db import models
from django.urls import reverse

# Create your models here.


class Service(models.Model):
    name = models.CharField('Name', max_length=200, help_text='Enter a service (eg. change tires)')

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    price = models.CharField('Price', max_length=10, help_text='Price of service')

    def __str__(self):
        return f'{self.service.name} - {self.price} eur'

    def get_absolute_url(self):
        return reverse('serviceprice-detail', args=[str(self.id)])


class ModelCar(models.Model):
    brand = models.CharField('Brand', max_length=40, help_text='Car brand')
    model = models.CharField('Model', max_length=40, help_text='Car model')
    engine = models.CharField('Engine', max_length=10, help_text='Car engine')

    def __str__(self):
        return f'{self.brand} {self.model} {self.engine}'


class ServiceCar(models.Model):
    service_price = models.ForeignKey('ServicePrice', on_delete=models.SET_NULL, null=True)
    car_model = models.ForeignKey('ModelCar', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.car_model.brand} {self.car_model.model} {self.car_model.engine} - {self.service_price.name} {self.service_price.price}'

    def get_absolute_url(self):
        return reverse('servicecar-detail', args=[str(self.id)])



class Car(models.Model):
    client = models.CharField('Client', max_length=40, help_text='Client name')
    car_model = models.ForeignKey('ModelCar', on_delete=models.SET_NULL, null=True)
    license_plate = models.CharField('Client', max_length=7, help_text='3 letters and 3 numbers with a space in between'
                                                        ' <a href="https://www.regitra.lt/lt/paslaugos/numerio-zenklai/numerio-zenklu-tipai-ir-ju-aprasymai/bendrojo-naudojimo">License plate info</a>')
    vin_code = models.CharField('Client', max_length=17, help_text='eg. 1HGCM82633A004352 <a href="https://www.autodna.lt/vin-numeris">VIN code info</a>')

    def __str__(self):
        return f'{self.client} {self.car_model.model} {self.license_plate} {self.vin_code}'

    def get_absolute_url(self):
        return reverse('car-detail', args=[str(self.id)])


class Order(models.Model):
    client_car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
    price = models.CharField('Price', max_length=10, help_text='Price of repair')

    def __str__(self):
        return f'{self.client_car.license_plate} {self.price}'

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])


class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    amount = models.CharField('Amount', max_length=10, help_text='Price of repair')
    price = models.CharField('Price', max_length=10, help_text='Price of repair')

    def __str__(self):
        return f'{self.order.client_car.license_plate} {self.service.name} {self.amount} {self.price}'

    def get_absolute_url(self):
        return reverse('orderline-detail', args=[str(self.id)])