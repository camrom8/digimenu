from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('liq/checkout', views.cart_detail_liqour, name='cart_detail_liq'),
    path('add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('delivery/', views.DeliveryDetails.as_view(), name='cart_delivery'),
    path('liq/delivery/', views.DeliveryDetailsLiqour.as_view(), name='cart_delivery_liq'),
]