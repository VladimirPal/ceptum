          # -*- coding: utf-8 -*-
from django import forms
from models import STATUS_CHOICES
from django.contrib.auth.models import User

class ClientForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact_name = forms.CharField(max_length=300)
    email = forms.EmailField(max_length=100, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    status_time = forms.DateTimeField(required=False)
    status_comment = forms.CharField(max_length=500, required=False)
    data = forms.CharField(widget=forms.Textarea,required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())
    file_name = forms.CharField(max_length=50, required=False)
    file = forms.FileField(required=False)

