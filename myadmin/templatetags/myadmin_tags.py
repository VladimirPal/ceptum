          # -*- coding: utf-8 -*-
from django import template
from datetime import date
from cart.models import Client, STATUS_CHOICES
from myadmin.models import Cash

register = template.Library()

def spanning_months(start, end):
    assert start <= end
    current = start.year * 12 + start.month - 1
    end = end.year * 12 + end.month - 1
    while current <= end:
        yield date(current // 12, current % 12 + 1, 1)
        current += 1

@register.inclusion_tag("myadmin/tags/date_tags.html")
def date_tags(request_path):
    if 'sales' in request_path:
        latest_client = Client.objects.all().latest('id').ordered_at
        first_client = Client.objects.order_by()[0].ordered_at
        dates = spanning_months(first_client, latest_client)

    elif 'cash' in request_path:
        latest_client = Cash.objects.all().latest('id').date
        first_client = Cash.objects.order_by()[0].date
        dates = spanning_months(first_client, latest_client)

    return {
        'dates': dates,
        'request_path' : request_path
        }

@register.inclusion_tag("myadmin/tags/menu.html")
def menu(request):
    return {
        'request' : request,
        }

@register.simple_tag
def status_count(status):
    count = Client.objects.filter(status=status).count()
    if status == "PROCESS":
        status_with_count = "Обработать(" + str(count) + ')'
    elif status == "POSTSEND":
        status_with_count = "Отправить почтой(" + str(count) + ')'
    elif status == "POSTSENDED":
        status_with_count = "Отправлено почтой(" + str(count) + ')'
    elif status == "COURIER_SEND":
        status_with_count = "Отправить курьером(" + str(count) + ')'
    elif status == "COURIER_TAKE":
        status_with_count = "Передано курьеру(" + str(count) + ')'
    elif status == "WAYT_PRODUCT":
        status_with_count = "Ожидание поступления товара(" + str(count) + ')'
    elif status == "BUYER_TAKE":
        status_with_count = "Передано покупателю(" + str(count) + ')'
    elif status == "BACK":
        status_with_count = "Обмен/Возврат(" + str(count) + ')'
    elif status == "CONTACT_AT":
        status_with_count = "Связаться(" + str(count) + ')'
    elif status == "REFUSED":
        status_with_count = "Снятие заявки клиентом(" + str(count) + ')'
    elif status == "CASH_IN":
        status_with_count = "Деньги внесены(" + str(count) + ')'
    else:
        status_with_count = status
    return status_with_count

@register.inclusion_tag("myadmin/tags/select.html")
def select(client):
    return {
        'need_statuses': STATUS_CHOICES,
        'client' : client,
        }
