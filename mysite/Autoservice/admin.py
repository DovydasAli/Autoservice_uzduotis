from django.contrib import admin
from .models import Service, CarService, ServicePrice, CarModel, Car, Order, OrderLine

# Register your models here.

admin.site.register(Service)
admin.site.register(CarService)
admin.site.register(ServicePrice)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)
