from django.urls import path
from parking import views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('car_in/', views.car_in, name='car_in'),
    path('car_out/', views.car_out, name='car_out'),
    path('success_in/', views.success_in, name='success_in'),
    path('success_out/', views.success_out, name='success_out'),
]
