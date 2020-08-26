from django.shortcuts import render
from django.views.generic import ListView, DetailView

from menus.models import Menu


class MenuList(ListView):
    """View for displaying all menus"""
    model = Menu
    template_name = "account/dashboard.html"
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(owner=user)


