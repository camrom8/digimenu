from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('search', views.Index.as_view(), name='search'),
    path('test', views.TestPage.as_view(), name='test'),
    path('donlicor', views.DonLicor.as_view(), name='don-licor'),
]
