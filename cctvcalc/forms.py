        # -*- coding: utf-8 -*-
from django import forms
from cctvcalc.models import SYSTEM_TYPE_CHOICES, RECORDER_TIME_CHOICES, SPEED_RECORD_CHOICES, IpCams, CalcCart

class TypeForm(forms.Form):
    system_type = forms.ChoiceField(choices=SYSTEM_TYPE_CHOICES, widget=forms.RadioSelect)

IS_IP_CHOICES = (
    ('0', u'Аналоговое'),
    ('1', u'IP'),
    )

class IpForm(forms.Form):
    is_ip = forms.ChoiceField(choices=IS_IP_CHOICES, widget=forms.RadioSelect)

class RecorderForm(forms.Form):
    recorder_time = forms.ChoiceField(choices=RECORDER_TIME_CHOICES)
    speed_record = forms.ChoiceField(choices=SPEED_RECORD_CHOICES, required=False)

class MicForm(forms.Form):
    count_microfone = forms.IntegerField(required=False)

class InstallForm(forms.Form):
    cable_length = forms.CharField(required=False)

class IpCamForm(forms.ModelForm):
    cart = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=CalcCart.objects.all())
    class Meta:
        model = IpCams
