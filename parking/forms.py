from django import forms
from parking.models import *


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('car_number',)
        labels = {
            'car_number': '자동차 번호',
        }


class CalcForm(forms.Form):
    pay_balance = forms.CharField(max_length=15)


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['ticket_limit'].widget.attrs['readonly'] = True

    class Meta:
        model = Car
        fields = ('car_num', 'ticket_num', 'ticket_limit')
        labels = {
            'car_num': '자동차 번호',
            'ticket_num': '정기권 번호',
            'ticket_limit': '정기권 기한'
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'name': '이름',
            'phone': '전화번호',
            'email': '이메일'
        }