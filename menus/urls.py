from django.urls import path
from . import views

app_name = "menu"
urlpatterns = [
    path('test/', views.ViewTest.as_view(), name='test'),
    path('upload_menu/', views.menu_upload, name='upload'),
    path('upload_size/', views.size_upload, name='upload-size'),
    path('upload_add_ons/', views.add_ons_upload, name='upload-add_ons'),
    path('price/<int:item_id>', views.item_prices_get, name='price'),
    path('adds_on/<int:item_id>', views.get_adds_on, name='adds-on'),
    path('same_item/<int:item_id>', views.same_items_in_cart, name='same-item'),
    path('order/<int:item_id>', views.item_to_order, name='order'),
    path('list/<str:city>/', views.MenuList.as_view(), name='list'),
    path('create/', views.MenuCreate.as_view(), name='create'),
    path('item_create/', views.ItemCreate.as_view(), name='item-create'),
    path('item_update/<int:pk>', views.ItemUpdate.as_view(), name='item-update'),
    path('item_delete/<int:pk>', views.ItemDelete.as_view(), name='item-delete'),
    path('get_category_items/<int:cat_id>', views.get_category_items, name='get-items'),
    path('category_create/', views.CategoryCreate.as_view(), name='category-create'),
    path('category_update/<int:pk>', views.CategoryUpdate.as_view(), name='category-update'),
    path('category_delete/<int:pk>', views.CategoryDelete.as_view(), name='category-delete'),
    path('ad_update/<int:pk>', views.AdUpdate.as_view(), name='ad-update'),
    path('count_visit/', views.menu_access_count, name='count'),
    path('establishment_create/', views.EstablishmentCreate.as_view(), name='establishment-create'),
    path('<slug:title_slug>/edit/', views.MenuEditDetails.as_view(), name='edit'),
    path('<slug:title_slug>/edit/<int:partial>', views.MenuEditDetails.as_view(), name='edit-partial'),
    path('<slug:title_slug>/', views.MenuDetails.as_view(), name='details'),
]
