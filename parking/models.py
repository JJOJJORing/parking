from django.db import models
from datetime import datetime, timedelta


class User(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField('Email')

    def __str__(self):
        return self.name


class Car(models.Model):
    car_num = models.CharField(max_length=10)
    ticket_num = models.CharField(max_length=10)
    ticket_limit = models.DateField(default=(datetime.now() + timedelta(weeks=12)))
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.car_num


class Log(models.Model):
    car_number = models.CharField(max_length=10)
    car_in = models.DateTimeField(auto_now_add=True)
    car_out = models.DateTimeField(auto_now=True)
    user_stat = models.NullBooleanField()
    pay_val = models.CharField(max_length=50, blank=True, null=True)
    car_stat = models.NullBooleanField()

    def __str__(self):
        return self.car_number
