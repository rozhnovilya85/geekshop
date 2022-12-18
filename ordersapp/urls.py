from django.urls import path
from ordersapp import views as ordersapp
app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('create/', ordersapp.CreateListView.as_view(), name='create'),
    path('update/<pk>/', ordersapp.UpdateListView.as_view(), name='update'),
    path('read/<pk>/', ordersapp.DetailListView.as_view(), name='read'),
    path('delete/<pk>/', ordersapp.DeleteListView.as_view(), name='delete'),
    path('complete/<pk>/', ordersapp.complete, name='complete'),
    path('product/<pk>/price/', ordersapp.get_product_price, name='product_price'),

]