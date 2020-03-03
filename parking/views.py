from django.shortcuts import render, redirect
from parking.forms import *
from parking.models import Car, User, Log
import math
from django.http import HttpResponse


def car_in(request):
    if request.method == "POST":
        if request.POST.get('carin') == '입차':
            form = LogForm(request.POST)
            if form.is_valid():
                log = form.save(commit=False)

                user_car = Car.objects.filter(car_num=log.car_number)
                log_latest = Log.objects.filter(car_number=log.car_number).order_by('-car_in')[0]
                if log_latest.pay_val:
                    if user_car.filter(ticket_limit__gt=timezone.now()):
                        log.user_stat = True
                    else:
                        log.user_stat = False
                    log.save()
                    return redirect('success_in/')
                else:
                    return HttpResponse('오류입니다')
        else:
            form = LogForm(request.POST)
            if form.is_valid():
                log = form.save(commit=False)
                log_recent = Log.objects.filter(car_number=log.car_number).order_by('-car_out')[0]
                log_recent.car_out = timezone.now()
                out_time = log_recent.car_out
                log_recent.save()

                if log_recent.user_stat and log_recent.pay_val is None:
                    log_recent.pay_val = 'ticket'
                    log_recent.save()
                    return redirect('success_out/')
                else:
                    in_time = log_recent.car_in
                    value = out_time - in_time
                    log_recent.pay_val = math.ceil(value.seconds/60)*10
                    log_recent.save()
                    return redirect('success_out/')
    else:
        form = LogForm()
    return render(request, 'parking/index.html', {'form': form})