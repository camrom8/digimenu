from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from menus.helpers.choices import SIZES, NONE


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
    title = models.CharField(_('title'), max_length=30)
    subtitle = models.CharField(_('subtitle'), max_length=50)
    description = models.TextField(_('description'), max_length=500)
    logo = models.ImageField(_('logo'), blank=True)

    def __str__(self):
        return self.title


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
    ingredients = models.CharField(_('ingredients'), max_length=127)
    description = models.CharField(_('description'), max_length=255)
    photo = models.ImageField(_('photo'), blank=True)

    def __str__(self):
        return self.name


class Establishment(models.Model):
    """Database model for Establishments"""
    type = models.CharField(_('type'), max_length=30)

    def __str__(self):
        return self.type


class Category(models.Model):
    """Database model for Establishments"""
    name = models.CharField(_('name'), max_length=30)

    def __str__(self):
        return self.name


class Price(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(_('price_num'), decimal_places=0, max_digits=6)
    price_str = models.CharField(_('price'), max_length=10)
    size = models.CharField(max_length=20, choices=SIZES, default=NONE)

    def __str__(self):
        return f'price for {self.item}'
