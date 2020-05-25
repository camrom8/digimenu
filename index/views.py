from django.shortcuts import render
from django.views import View
from .forms import SearchBarForm


class Index(View):
    """home page view"""
    def get(self, request):
        """render home page"""
        form = SearchBarForm()
        return render(request, "index/details3.html", {'page': 'home', 'form': form})
