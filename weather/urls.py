from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<float:lat>,<float:lon>/', views.forecast, name='forecast'),
]
