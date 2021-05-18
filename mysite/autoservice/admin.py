from django.contrib import admin
from .models import Service, Car, OwnerCar, Order, OrderLine, OrderReview, Profile

# Register your models here.


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    search_fields = ('licence_plate', 'vin_code')
    can_delete = False
    extra = 0


class CarAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'engine')


class OwnerCarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'year', 'car', 'licence_plate', 'vin_code')
    search_fields = ('licence_plate', 'vin_code')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner_car', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    inlines = [OrderLineInline]


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'qty')
    list_editable = ('service', 'qty')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price', )


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')


admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(OwnerCar, OwnerCarAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(Profile)
