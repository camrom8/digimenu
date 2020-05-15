from django.contrib import admin
from django.db import models

from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellido")
    email = models.EmailField(null=True, blank=True)
    phone = models.BigIntegerField(verbose_name="telefono")
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Dirección")
    #postal_code = models.CharField(max_length=200)
    #city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado")
    send = models.BooleanField(default=False, verbose_name="entregado")
    paid = models.BooleanField(default=False, verbose_name="pagado")

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
