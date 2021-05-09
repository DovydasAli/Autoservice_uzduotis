from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, Order, OrderLine, Car, OwnerCar
from django.shortcuts import render, get_object_or_404
from django.views import generic

# Create your views here.

def index(request):

    num_cars = Car.objects.all().count()
    num_orders = Order.objects.all().count()
    num_services = Service.objects.all().count()

    num_orders_done = Order.objects.filter(status__exact='done').count()

    context = {
        'num_cars': num_cars,
        'num_orders': num_orders,
        'num_orders_done': num_orders_done,
        'num_services': num_services,
    }

    return render(request, 'index.html', context=context)


def cars(request):
    cars = OwnerCar.objects.all()
    context = {
        'cars': cars
    }
    print(cars)
    return render(request, 'cars.html', context=context)

def car(request, car_id):
    single_car = get_object_or_404(OwnerCar, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'