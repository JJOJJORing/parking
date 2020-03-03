from django.urls import path
from parking import views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('car_in/', views.car_in, name='car_in')
]