from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:lat>,<slug:lon>/', views.forecast, name='forecast'),
    path('random/', views.random, name='random'),
]
