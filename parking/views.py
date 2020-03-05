from django.shortcuts import render, redirect
from parking.forms import *
from parking.models import Car, User, Log
from django.core.exceptions import ObjectDoesNotExist
import math
from django.utils import timezone
from django.http import HttpResponseRedirect


def index(request):
    form = LogForm()
    return render(request, 'parking/index.html', {'form': form})


# def success_in(request):
#     return render(request, 'parking/success_in.html', {})


# def success_out(request):
#     return render(request, 'parking/success_out.html', {})


def car_in(request):
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            try:
                user_car = Car.objects.get(car_num=log.car_number, ticket_limit__gte=timezone.now())
                log.user_stat = True
                log.pay_val = 'ticket'
                log.car_stat = True
                log.save()
                context = {
                    'customer': user_car.user.name,
                    'in_time': log.car_in,
                    'ticket_limit': user_car.ticket_limit
                }
            except ObjectDoesNotExist as e:
                log.user_stat = False
                log.car_stat = True
                log.save()
                context = {
                    'customer': '고객',
                    'in_time': log.car_in,
                }

            return render(request, 'parking/success_in.html', context)
    else:
        form = LogForm()
        return render(request, 'parking/index.html', {'form': form})


def calculate(request):
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
                    user = Car.objects.get(car_num=log_recent.car_number)
                    context = {
                        'customer': user.user.name,
                        'out_time': log_recent.car_out,
                    }
                    return render(request, 'parking/success_out.html', context)
                else:
                    out_time = timezone.now()
                    log_recent.car_out = out_time
                    log_recent.save()
                    car_number = log.car_number
                    return HttpResponseRedirect('./{}/'.format(car_number))
            except ObjectDoesNotExist as e:
                print(e)
                form = LogForm()
                return render(request, 'parking/index.html', {'form': form})
    else:
        form = LogForm()
        return render(request, 'parking/index.html', {'form': form})


def car_out(request, car_number):
    guest_car = Log.objects.get(car_number=car_number, car_stat=True)
    out_time = guest_car.car_out
    in_time = guest_car.car_in
    pay_val = math.ceil((out_time - in_time).seconds / 60) * 100
    if request.method == 'POST':
        form = CalcForm(request.POST)
        if form.is_valid():
            pay_balance = form.cleaned_data['pay_balance']
            try:
                if pay_balance == str(pay_val):
                    guest_car.car_stat = False
                    guest_car.pay_val = pay_val
                    guest_car.save()
                    context = {
                        'out_time': out_time,
                        'pay_value': pay_balance
                    }
                    return render(request, 'parking/success_out.html', context)
                else:
                    return redirect('./')
            except ObjectDoesNotExist as e:
                form = CalcForm()
                context = {
                    'car_number': car_number,
                    'form': form,
                    'pay_balance': pay_val,
                }
                return render(request, 'parking/calc.html', context)

    else:
        form = CalcForm()
        context = {
            'car_number': car_number,
            'form': form,
            'pay_balance': pay_val,
        }
        return render(request, 'parking/calc.html', context)
