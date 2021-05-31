from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path('myorders/', views.CarsInShopByUserListView.as_view(), name='my-orders'),
    path('myorders/<int:pk>', views.CarsInShopByUserDetailView.as_view(), name='my-order'),
    path('myorders/new', views.CarsInShopByUserCreateView.as_view(), name='my-order-new'),
    path('myorders/<int:pk>/update', views.CarsInShopByUserUpdateView.as_view(), name='my-order-update'),
    path('myorders/<int:pk>/delete', views.CarsInShopByUserDeleteView.as_view(), name='my-order-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('i18n/', include('django.conf.urls.i18n')),
]
