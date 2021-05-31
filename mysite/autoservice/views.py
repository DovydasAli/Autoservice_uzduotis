from django.http import HttpResponse
from .models import Service, Order, OrderLine, Car, OwnerCar

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from .forms import OrderReviewForm, UserUpdateForm, ProfileUpdateForm
from django.utils.translation import gettext as _

# Create your views here.

def index(request):
    num_cars = Car.objects.all().count()
    num_orders = Order.objects.all().count()
    num_services = Service.objects.all().count()

    num_orders_done = Order.objects.filter(status__exact='done').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cars': num_cars,
        'num_orders': num_orders,
        'num_orders_done': num_orders_done,
        'num_services': num_services,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def cars(request):
    paginator = Paginator(OwnerCar.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    return render(request, 'cars.html', context=context)

def car(request, car_id):
    single_car = get_object_or_404(OwnerCar, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(ListView):
    model = Order
    paginate_by = 3
    template_name = 'order_list.html'

class OrderDetailView(FormMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    form_class = OrderReviewForm

    class Meta:
        ordering = ['title']

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderReviewForm(initial={'order': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


class CarsInShopByUserListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_cars.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(owner_car__owner=self.request.user).order_by('due_date')


def search(request):
    query = request.GET.get('query')
    search_results = Order.objects.filter(Q(owner_car__owner__username__icontains=query) | Q(owner_car__car__model__icontains=query) | Q(owner_car__licence_plate__icontains=query) | Q(owner_car__vin_code__icontains=query))
    return render(request, 'search.html', {'orders': search_results, 'query': query})

class CarsInShopByUserDetailView(LoginRequiredMixin,FormMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'user_car.html'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('my-order', kwargs={'pk': self.object.id})

    # įtraukiame formą į kontekstą, inicijuojame pradinę 'book' reikšmę.
    def get_context_data(self, *args, **kwargs):
        context = super(CarsInShopByUserDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderReviewForm()
        return context

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(CarsInShopByUserDetailView, self).form_valid(form)

class CarsInShopByUserCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['owner_car', 'due_date']
    success_url = "/autoservice/myorders/"
    template_name = 'user_order_form.html'

    def get_form(self, *args, **kwargs):
        form = super(CarsInShopByUserCreateView, self).get_form(*args, **kwargs)
        form.fields['owner_car'].queryset = OwnerCar.objects.filter(owner=self.request.user)
        return form

class CarsInShopByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['owner_car', 'due_date']
    success_url = "/autoservice/myorders/"
    template_name = 'user_order_form.html'

    def get_form(self, *args, **kwargs):
        form = super(CarsInShopByUserUpdateView, self).get_form(*args, **kwargs)
        form.fields['owner_car'].queryset = OwnerCar.objects.filter(owner=self.request.user)
        return form

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner_car.owner

class CarsInShopByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = "/autoservice/myorders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner_car.owner

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %(username)s already taken!') % {'username': username})
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _(f'User with {email} has already been registered!'))
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, _('Passwords must match!'))
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _(f"Profile updated"))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)
