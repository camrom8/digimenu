from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from .forms import SearchBarForm


class Index(View):
    """home page view"""

    def get(self, request):
        """render home page"""
        form = SearchBarForm()
        return render(request, "index/index.html",
                      {'page': 'home', 'form': form})


class HomePage(TemplateView):
    template_name = "index/home.html"


class TestPage(TemplateView):
    template_name = "test.html"


class DonLicor(View):
    """Don Licor page view"""

    def get(self, request):
        return redirect("menu/donlicor")
