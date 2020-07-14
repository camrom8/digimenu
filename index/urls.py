from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('search', views.Index.as_view(), name='search'),
]
