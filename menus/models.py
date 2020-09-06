from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext as _

from menus.helpers.choices import SIZES, NONE, TEMPLATES, SLIDES


class Menu(models.Model):
    """ Database model for menus"""
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='menus',
                              verbose_name=_('owner')
                              )
    establishment = models.ForeignKey('Establishment',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      related_name='establishments',
                                      verbose_name=_('establishment')
                                      )
    title = models.CharField(_('title'), max_length=40, unique=True)
    title_slug = models.SlugField(unique=True)
    subtitle = models.CharField(_('subtitle'), max_length=50)
    description = models.TextField(_('description'), max_length=500)
    logo = models.ImageField(_('logo'), default="images/default/no_photo.png")
    template = models.CharField(max_length=30, choices=TEMPLATES, default=NONE)
    city = models.CharField(max_length=127, null=True, blank=True)
    address = models.CharField(max_length=127, null=True, blank=True)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        super(Menu, self).save(*args, **kwargs)


class Item(models.Model):
    """Database model for items"""
    menu = models.ForeignKey('Menu',
                             on_delete=models.CASCADE,
                             verbose_name=_('menu'),
                             related_name='items'
                             )
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name=_('category')
                                 )
    name = models.CharField(_('name'), max_length=30)
    ingredients = models.CharField(_('ingredients'), max_length=511, blank=True)
    description = models.CharField(_('description'), max_length=255, null=True, blank=True)
    photo = models.ImageField(_('photo'), default="images/default/no_photo.png")
    upload_code = models.PositiveIntegerField(_('upload code'), default=0, null=True)

    def __str__(self):
        return f'{self.name}-{self.menu}'


class Establishment(models.Model):
    """Database model for Establishments"""
    type = models.CharField(_('type'), max_length=30)

    def __str__(self):
        return self.type


class Category(models.Model):
    """Database model for Category"""
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='categories',
                              verbose_name=_('owner')
                              )
    menu = models.ForeignKey("Menu",
                              on_delete=models.CASCADE,
                              related_name='categories',
                              verbose_name=_('Menu'),
                              null=True
                              )
    name = models.CharField(_('name'), max_length=30)
    position = models.PositiveSmallIntegerField(_('position'), )

    class Meta:
        ordering = ['menu', 'position']

    def __str__(self):
        return f'{self.name}, {str(self.menu)}'


class Price(models.Model):
    """Database for size"""
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(_('price_num'), decimal_places=0, max_digits=6)
    price_str = models.CharField(_('price'), max_length=10)
    size = models.CharField(max_length=20, choices=SIZES, default=NONE)
    choice = models.BooleanField(default=False)
    half = models.BooleanField(default=False)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f'{self.item.menu}: {self.item}, {self.size}'


class ProductInCart(models.Model):
    price = models.ForeignKey('Price', on_delete=models.CASCADE, related_name='inCart')
    total = models.DecimalField(decimal_places=0, max_digits=6, null=True)
    add_on = models.ManyToManyField('AddsOn', through='Quantity')

    def __str__(self):
        return str(self.total)


class AddsOn(models.Model):
    product = models.ManyToManyField('Price', related_name='adds_ons')
    name = models.CharField(max_length=20)
    price = models.DecimalField(_('price_num'), decimal_places=0, max_digits=6)
    price_str = models.CharField(_('price'), max_length=10)

    def __str__(self):
        return self.name


class Quantity(models.Model):
    product = models.ForeignKey('ProductInCart', on_delete=models.CASCADE)
    addOn = models.ForeignKey('AddsOn', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(decimal_places=0, max_digits=6, null=True)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.addOn.price
        super(Quantity, self).save(*args, **kwargs)
