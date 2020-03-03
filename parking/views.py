from django.shortcuts import render, redirect
from parking.forms import *
from parking.models import Car, User, Log
from django.core.exceptions import ObjectDoesNotExist
import math


def index(request):
    form = LogForm()
    return render(request, 'parking/index.html', {'form': form})


def success_in(request):
    return render(request, 'parking/success_in.html', {})


def success_out(request):
    return render(request, 'parking/success_out.html', {})


def car_in(request):
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            try:
                user_car = Car.objects.get(car_num=log.car_number, ticket_limit__gte=timezone.now())
                log.user_stat = True
                log.pay_val = 'ticket'
            except ObjectDoesNotExist as e:
                log.user_stat = False
            log.car_stat = True
            log.save()
            return redirect('http://127.0.0.1:8000/parking/success_in/')
    else:
        form = LogForm()
        return render(request, 'parking/index.html', {'form': form})


def car_out(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            try:
                log = form.save(commit=False)
                log_recent = Log.objects.get(car_number=log.car_number, car_stat=True)
                user = log_recent.user_stat
                if user:
                    log_recent.car_out = timezone.now()
                    log_recent.car_stat = False
                    log_recent.save()
                else:
                    out_time = timezone.now()
                    in_time = log_recent.car_in
                    value = math.ceil((out_time - in_time).seconds / 60) * 100
                    log_recent.car_out = out_time
                    log_recent.car_stat = False
                    log_recent.pay_val = value
                    log_recent.save()

                return redirect('http://127.0.0.1:8000/parking/success_out/')
            except Exception as e:
                print(e)
                return redirect('http://127.0.0.1:8000/parking/')
    else:
        form = LogForm(request.POST)
        return render(request, 'parking/index.html', {'form': form})
