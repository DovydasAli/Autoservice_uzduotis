from django.contrib import admin
from .models import Service, Car, OwnerCar, Order, OrderLine

# Register your models here.


admin.site.register(Service)
admin.site.register(Car)
admin.site.register(OwnerCar)
admin.site.register(Order)
admin.site.register(OrderLine)