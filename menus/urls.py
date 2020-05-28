from django.urls import path
from . import views

app_name = "menu"
urlpatterns = [
    path('test/', views.ViewTest.as_view(), name='test'),
    path('price/<int:item_id>', views.item_prices_get, name='price'),
    path('<slug:title_slug>/', views.MenuDetails.as_view(), name='details'),
    path('create/', views.MenuCreate.as_view(), name='create'),
    path('list/', views.MenuList.as_view(), name='list'),
    path('item_create/', views.ItemCreate.as_view(), name='item-create'),
    path('category_create/', views.CategoryCreate.as_view(), name='category-create'),
    path('establishment_create/', views.EstablishmentCreate.as_view(), name='establishment-create'),
]
