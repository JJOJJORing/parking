from django import forms
from parking.models import *


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('car_number',)