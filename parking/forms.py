from django import forms
from parking.models import *


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('car_number',)


class CalcForm(forms.Form):
    pay_balance = forms.CharField(max_length=15)