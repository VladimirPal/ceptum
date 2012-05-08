# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from myadmin.models import Client
from myadmin.models import STATUS_CHOICES

class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('comment')
