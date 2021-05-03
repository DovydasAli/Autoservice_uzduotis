from django.contrib import admin
from .models import Service, ServiceCar, ServicePrice, ModelCar, Car, Order, OrderLine

# Register your models here.

admin.site.register(Service)
admin.site.register(ServiceCar)
admin.site.register(ServicePrice)
admin.site.register(ModelCar)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)
