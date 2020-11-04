from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('watch_stock.html', views.watch_stock, name="watch_stock"),
    path('delete/<symbol>', views.delete, name="delete")
]