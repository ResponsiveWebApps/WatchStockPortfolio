from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('stock_info.html', views.stock_info, name="stock_info"),
    path('watch_stock.html', views.watch_stock, name="watch_stock"),
    path('delete/<symbol>', views.delete, name="delete"),
    path('signup.html', views.signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate')
]