from django.urls import path
from . import views

app_name = "menu"
urlpatterns = [
    path('test/', views.ViewTest.as_view(), name='test'),
    path('upload_menu/', views.menu_upload, name='upload'),
    path('upload_size/', views.size_upload, name='upload-size'),
    path('price/<int:item_id>', views.item_prices_get, name='price'),
    path('adds_on/<int:item_id>', views.get_adds_on, name='adds-on'),
    path('same_item/<int:item_id>', views.same_items_in_cart, name='same-item'),
    path('order/<int:item_id>', views.item_to_order, name='order'),
    path('list/<str:city>/', views.MenuList.as_view(), name='list'),
    path('<slug:title_slug>/', views.MenuDetails.as_view(), name='details'),
    path('create/', views.MenuCreate.as_view(), name='create'),
    path('item_create/', views.ItemCreate.as_view(), name='item-create'),
    path('category_create/', views.CategoryCreate.as_view(), name='category-create'),
    path('establishment_create/', views.EstablishmentCreate.as_view(), name='establishment-create'),
]
