from django.urls import path
from parking import views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('car_in/', views.car_in, name='car_in_error'),
    path('calculate/', views.calculate, name='calc'),
    path('calculate/<str:car_number>/', views.car_out, name='calc_carnum'),
    path('register/', views.register, name='register')
]
