# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from myadmin.models import Client
from django.contrib.auth.models import User
from fields import UserModelChoiceField

STATUS_CHOICES = (
    ('CALL', 'Созвон'),
    ('OFFER', 'Скинуть КП'),
    ('INSPECTION', 'Осмотр'),
    )

class ClientForm(ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'input-xlarge'}))
    contact_name = forms.CharField(widget=forms.Textarea(attrs={'rows':'3', 'class':'input-xlarge'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'type':'email', 'class':'input-xlarge'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
    status_date = forms.DateField(input_formats=['%d/%m/%Y'], required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    status_time = forms.TimeField(required=False, widget=forms.TextInput(attrs={'class':'time_input', 'size':'5', 'max_length':'5', 'style':'display:none; width:40px;'}))
    status_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3', 'class':'input-xlarge'}))
    data = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3', 'class':'input-xxlarge'}))
    user = UserModelChoiceField(queryset=User.objects.filter(groups__name='Менеджеры'))
    class Meta:
        model = Client
        exclude = ('comment')

