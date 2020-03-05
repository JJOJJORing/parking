from django.urls import path
from parking import views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('car_in/', views.car_in, name='car_in'),
    path('car_out/', views.car_out, name='car_out'),
    path('calculate/', views.calculate, name='calc'),
    path('calculate/<str:car_number>/', views.car_out, name='calc_carnum')
]
