from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    price = models.FloatField(_("Price"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Car(models.Model):
    manufacturer = models.CharField(_('Manufacturer'), max_length=200)
    model = models.CharField(_('Model'), max_length=200)
    engine = models.CharField(_('Engine'), max_length=200)

    def __str__(self):
        return f"{self.manufacturer} {self.model}, {self.engine}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class OwnerCar(models.Model):
    year = models.IntegerField(_('Year'), null=True)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey('Car', verbose_name=_("Car"), on_delete=models.SET_NULL, null=True)
    licence_plate = models.CharField(_('Licence plate'), max_length=200)
    vin_code = models.CharField(_('VIN code'), max_length=200)
    description = HTMLField(null=True, blank=True)
    picture = models.ImageField(_('Car photo'), upload_to='cars', null=True)

    def __str__(self):
        return f"{self.owner}: {self.car}, {self.year}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = _('Owner Car')
        verbose_name_plural = _('Owners Cars')


class Order(models.Model):
    owner_car = models.ForeignKey('OwnerCar', verbose_name=_("Clients' car"), on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(_('Due Date'), null=True, blank=True)

    STATUS = (
        ('draft', _('Draft')),
        ('in progress', _('In progress')),
        ('done', _('Done')),
        ('canceled', _('Canceled')),
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
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

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

    def get_absolute_url(self):
        """Nurodo konkretaus apra??ymo galin?? adres??"""
        return reverse('order-detail', args=[str(self.id)])


class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey('Service', verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(_("Quantity"))

    @property
    def service_cost(self):
        return self.service.price * self.qty

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')


class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(_('Comment'), max_length=2000)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
