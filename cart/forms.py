          # -*- coding: utf-8 -*-
from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='Имя*', error_messages={'required':'Имя обязательно для заполнения'})
    surname = forms.CharField(required=False, label='Фамилия')
    patronymic = forms.CharField(required=False, label='Отчество')
    city = forms.CharField(required=False, label='Город')
    postcode = forms.IntegerField(required=False, label='Индекс')
    phone = forms.CharField(label='Телефон*', error_messages={'required':'Телефон обязателен для заполнения'})
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'2'}), label='Адрес')
    email = forms.EmailField(required=False)
