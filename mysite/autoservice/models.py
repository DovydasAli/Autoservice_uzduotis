from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.


class Service(models.Model):
    name = models.CharField('Name', max_length=200)
    price = models.FloatField("Price")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Car(models.Model):
    manufacturer = models.CharField('Manufacturer', max_length=200)
    model = models.CharField('Model', max_length=200)
    engine = models.CharField('Engine', max_length=200)

    def __str__(self):
        return f"{self.manufacturer} {self.model}, {self.engine}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class OwnerCar(models.Model):
    year = models.IntegerField('Year', null=True)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey('Car', verbose_name="Car", on_delete=models.SET_NULL, null=True)
    licence_plate = models.CharField('Licence plate', max_length=200)
    vin_code = models.CharField('VIN code', max_length=200)
    description = HTMLField(null=True, blank=True)
    picture = models.ImageField('Car photo', upload_to='cars', null=True)

    def __str__(self):
        return f"{self.owner}: {self.car}, {self.year}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = 'Owner Car'
        verbose_name_plural = 'Owners Cars'


class Order(models.Model):
    owner_car = models.ForeignKey('OwnerCar', verbose_name="Clients' car", on_delete=models.SET_NULL, null=True)
    due_date = models.DateField('Due Date', null=True, blank=True)

    STATUS = (
        ('draft', 'Draft'),
        ('in progress', 'In progress'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS,
        blank=True,
        default='draft',
        help_text='Status',
    )

    def __str__(self):
        return f"{self.owner_car}: {self.due_date}, {self.status}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    @property
    def is_overdue(self):
        if self.due_date and date.today() > self.due_date:
            return True
        return False

    @property
    def total_cost(self):
        order_line = OrderLine.objects.filter(order=self.id)
        total = 0

        for order in order_line:
            cost = order.service.price * order.qty
            total += cost
        return total



class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name="Order", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey('Service', verbose_name="Service", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField("Quantity")

    @property
    def service_cost(self):
        return self.service.price * self.qty

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'


class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self):
        super().save()
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
