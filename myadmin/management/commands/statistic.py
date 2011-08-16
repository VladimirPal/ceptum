          # -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import date
from myadmin.models import Cash, Cash_statistic, Product_statistic
from cart.models import Client, CartProduct
from myadmin.settings import EMS, COURIER

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = date.today()
        first_day_month = today.replace(day=1)
        # Получаю все денежные потоки за вчера
        cashs = Cash.objects.filter(date__month=today.month, date__year=today.year,date__day=today.day-1)
        for cash in cashs:
            if cash.cause == 'FROM_CLIENT':
                if cash.cashflow > 0:
                    if cash.comment.isdigit():
                        # Получаю последнюю запись статистики
                        try:
                            statistic = Cash_statistic.objects.filter(type=cash.cause).latest('id')
                        except Cash_statistic.DoesNotExist:
                            statistic = Cash_statistic(date=first_day_month, type=cash.cause, cash=0)
                        # Если сегодняшний месяц не совпадает с записанным
                        if statistic.date.month != today.month:
                            # Создаю новую запись в статистике
                            statistic = Cash_statistic()
                            statistic.date = first_day_month
                            statistic.cash = 0
                            statistic.type = cash.cause
                        # Получаю клиента с которого пришли деньги
                        client = Client.objects.get(id=cash.comment)
                        # Получаю все покупки клиента
                        products = CartProduct.objects.filter(cartitem=client.cart)
                        for product in products:
                            # Получаю запись статистики
                            try:
                                product_statistic = Product_statistic.objects.filter(date__month=today.month,product=product.product).latest('id')
                            # Если такого товара еще нету то создаю его
                            except Product_statistic.DoesNotExist:
                                product_statistic = Product_statistic(date=first_day_month, product=product.product, quantity=0, cash=0)
                                product_statistic.save()
                            # Если сегодняшний месяц не совпадает с записанным
                            if statistic.date.month != today.month:
                                # Создаю новую запись в статистике
                                product_statistic = Product_statistic(date=first_day_month, product=product.product, quantity=0, cash=0)
                            # Делаю статистику по количеству
                            product_statistic.quantity += product.quantity
                            # Подсчитываю прибыль с проданного
                            profit = (product.product.price - product.product.wholesale_price)*product.quantity - client.discount
                            if client.delivery == 'EMS':
                                profit += EMS
                            elif client.delivery == 'COURIER':
                                profit -= COURIER
                            statistic.cash += profit
                            product_statistic.cash += profit
                            product_statistic.save()
                        statistic.save()
            else:
                # Получаю последнюю запись статистики
                try:
                    statistic = Cash_statistic.objects.filter(type=cash.cause).latest('id')
                except Cash_statistic.DoesNotExist:
                    statistic = Cash_statistic(date=first_day_month, type=cash.cause, cash=0)
                # Если сегодняшний месяц и год не совпадает с записанным
                if statistic.date.month != today.month:
                    # Создаю новую запись в статистике
                    statistic = Cash_statistic()
                    statistic.date = first_day_month
                    statistic.cash = 0
                    statistic.type = cash.cause
                statistic.cash += -cash.cashflow
                statistic.save()
