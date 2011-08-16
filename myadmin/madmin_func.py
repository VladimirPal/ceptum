          # -*- coding: utf-8 -*-
from cart.models import Client, CartProduct
from datetime import date, timedelta
import re, urllib, urllib2
from hashlib import md5
import decimal
from catalog.models import Product
from cart.settings import DISCOUNT, DISCOUNT_PERCENT, COUNT_FOR_DISCOUNT
from settings import *
from models import Cash, Balance
from forms import CashForm

# Возвращает число понедельника и воскресенья текущей недели
def week_boundaries(year, week):
    start_of_year = date(year, 1, 1)
    now = start_of_year + timedelta(weeks=week)
    mon = now - timedelta(days=now.weekday())
    sun = mon + timedelta(days=6)
    return mon, sun

# Список клиентов за запрошенный период времени
def clients_list(when):
        today = date.today()
        if when == 'today':
            clients = Client.objects.filter(ordered_at__year=today.year, ordered_at__month=today.month, ordered_at__day=today.day)
        elif when == 'week':
            monday, sunday = week_boundaries(today.year, int(today.strftime("%W")))
            clients = Client.objects.filter(ordered_at__year=today.year, ordered_at__month=today.month, ordered_at__range=(monday,sunday))
        elif when == 'month':
            clients = Client.objects.filter(ordered_at__year=today.year, ordered_at__month=today.month)
        elif when == 'year':
            clients = Client.objects.filter(ordered_at__year=today.year)
        elif when == 'all':
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(ordered_at__year=when[-4:], ordered_at__month=when[:-4])
        return clients

# Список денежных потоков за запрошенный период времени
def cash_list(when):
    today = date.today()
    if when == 'today':
        cash = Cash.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
    elif when == 'week':
        monday, sunday = week_boundaries(today.year, int(today.strftime("%W")))
        cash = Cash.objects.filter(date__year=today.year, date__month=today.month, date__range=(monday, sunday))
    elif when == 'month':
        cash = Cash.objects.filter(date__year=today.year, date__month=today.month)
    elif when == 'year':
        cash = Cash.objects.filter(date__year=today.year)
    else:
        cash = Cash.objects.filter(date__year=when[-4:], date__month=when[:-4])
    return cash

# Отправка смс с tracking number клиенту
def client_sms(newform):
    login = 'palv1@yandex.ru'
    password = '97ajhJaj9zna'
    phone = re.sub("\D", "", newform.phone)
    from_phone = "79151225291"
    msg = u"Здравствуйте, посылка с вашим заказом выслана. Номер отправления: %s Отследить посылку можно на сайте emspost.ru С Уважением my-spy.ru" % newform.tracking_number
    msg = urllib.urlencode({'msg': msg.encode('cp1251')})
    urllib2.urlopen('http://sms48.ru/send_sms.php?login=%s&to=%s&%s&from=%s&check2=%s' % (login, phone, msg.encode('cp1251'), from_phone, md5(login + md5(password).hexdigest() + phone).hexdigest()) )

# Обновляет количество товара на складе
def update_store(data, products, status_refused):
    # Предыдущий список товара
    products_name = []
    for product in products:
        products_name.append(product.product)
    # Текущий список товара
    newproducts_name = []
    # Если статус "Снятие заяки клиентом"
    if status_refused:
        for formitem in data:
            if formitem:
                product_name = formitem['product']
                quantity = formitem['quantity']
                # Обновляю количество товара на складе
                store_product = Product.objects.get(name=product_name)
                store_product.quantity += quantity
                store_product.save()
    else:
        for formitem in data:
            if formitem:
                product_name = formitem['product']
                quantity = formitem['quantity']
                # Обновление в случае удаления товара
                if formitem['DELETE']:
                    store_product = Product.objects.get(name=product_name)
                    store_product.quantity += quantity
                    store_product.save()
                else:
                    # Обновляю если у клиента еще нет товаров
                    if not products:
                        store_product = Product.objects.get(name=product_name)
                        store_product.quantity -= quantity
                        store_product.save()
                    else:
                        for product in products:
                            # Если такой товар у клиента уже есть
                            if product.product == product_name:
                                # Если количество совпадает то ничего не делаю
                                if product.quantity == quantity:
                                    pass
                                # Если количество изменилось - пишу изменения количества в складе
                                else:
                                    store_quantity = quantity - product.quantity
                                    store_product = Product.objects.get(name=product_name)
                                    store_product.quantity -= store_quantity
                                    store_product.save()
                    # Если добавился товар
                    if product_name not in products_name:
                        # Изменяю количество на складе
                        store_product = Product.objects.get(name=product_name)
                        store_product.quantity -= quantity
                        store_product.save()
                    # Обновляю текущий список товара
                    newproducts_name.append(product_name)
        # Сравниваю передыдущий список товара с текущим
        for product in products:
            # Если из предыдущего исчез товар
            if product.product not in newproducts_name:
                # Возвращаю его на склад
                store_product = Product.objects.get(name=product.product)
                store_product.quantity += product.quantity
                store_product.save()

# Высчитывает сумму и скидку
def subtotal(cartid):
    products = CartProduct.objects.filter(cartitem=cartid)
    cart_total = decimal.Decimal('0.00')
    cart_discount_total = 0
    discount = 0
    discount_quantity = 0
    for item in products:
        # Если на товар действует скидка
        if item.product.is_discount:
            # Высчитываю количество скидочных товаров
            discount_quantity += item.quantity
            # Общая стоимость скидочных товаров
            cart_discount_total += item.product.price * item.quantity
        # Общая стомость товаров без скидки
        cart_total += item.product.price * item.quantity
    # Если в настройках задана скидка то высчитываю
    if DISCOUNT:
        # Если товаров достаточно для скидки
        if discount_quantity >= COUNT_FOR_DISCOUNT:
            # Высчитываю скидку
            discount = (cart_discount_total * DISCOUNT_PERCENT)/100
        # Если скидочных товаров достсточно для скидки
        elif len(products) >= COUNT_FOR_DISCOUNT:
            # Высчитываю скидку
            discount = (cart_discount_total * DISCOUNT_PERCENT)/100
        cart_total -= discount
    ci = Client.objects.get(cart=cartid)
    ci.subtotal = cart_total
    ci.discount = discount
    ci.save()

def update_cash(data, client, client_status):
    # Если статус деньги внесены
    if data['status'] == 'CASH_IN':
        # Если предыдущий статус такой же, то ничего не делать
        if client_status == data['status']:
            pass
        # Если предыдущий статус был другой
        else:
            # Создаю денежный поток
            newcashflow = Cash()
            # Последний баланс
            last_balance = Cash.objects.all().latest('id')
            # Если доставка EMS
            if data['delivery'] == 'EMS':
                # Добавляю к стоимости 300 рублей
                newcashflow.cashflow = client.subtotal + EMS
                newcashflow.balance = last_balance.balance + client.subtotal + EMS
                newcashflow.comment = client.id
            # Если доставка курьером
            elif data['delivery'] == 'COURIER':
                # Вычитаю из стоимости 300 рублей
                newcashflow.cashflow = client.subtotal - COURIER
                newcashflow.balance = last_balance.balance + client.subtotal - COURIER
                newcashflow.comment = client.id
            else:
                # Бесплатная доставка
                newcashflow.cashflow = client.subtotal
                newcashflow.balance = last_balance.balance + client.subtotal
                newcashflow.comment = client.id
            newcashflow.cause = 'FROM_CLIENT'
            newcashflow.type = 'ENCASH'
            newcashflow.save()
            balance = Balance.objects.get(id=1)
            balance.encash += newcashflow.cashflow
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()
    else:
        # Если был изменен статус деньги внесены
        if client_status == 'CASH_IN':
            # Удаляю денежный поток и пересчитываю баланс
            cashflow = Cash.objects.get(comment=client.id)
            cashflows_recalc = Cash.objects.filter(pk__gt=cashflow.id).reverse()
            true_balance = cashflow.balance - cashflow.cashflow
            cashflow.delete()
            for cashflow_recalc in cashflows_recalc:
                cashflow_recalc.balance = true_balance + cashflow_recalc.cashflow
                true_balance = cashflow_recalc.balance
                cashflow_recalc.save()
            balance = Balance.objects.get(id=1)
            balance.encash -= cashflow.cashflow
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()

# Пересчитывает потоки исправляя остаток
def change_cashflows_balance(cash):
    cashflows_recalc = Cash.objects.filter(pk__gt=cash.id).reverse()
    true_balance = cash.balance
    for cashflow_recalc in cashflows_recalc:
        if cashflow_recalc.type == 'ENCASH':
            cashflow_recalc.balance = true_balance + cashflow_recalc.cashflow
            true_balance = cashflow_recalc.balance
            cashflow_recalc.save()
        else:
            cashflow_recalc.balance = true_balance
            cashflow_recalc.save()

# Изменяет и пересчитывает денежный поток
def change_cashflow(request, cash):
        # Предыдущий денежный поток
        last_cashflow = cash.cashflow
        # Предыдущий тип потока
        last_type = cash.type
        form = CashForm(request.POST, instance=cash)
        newform = form.save(commit=False)
        # Если новый поток не совпадает с предыдущим
        if not last_cashflow == newform.cashflow:
            balance = Balance.objects.get(id=1)
            # Если тип предыдущего потока "Наличные"
            if last_type == 'ENCASH':
                # Удаляю из баланса предыдуший поток
                balance.encash -= last_cashflow
                # Получаю разницу между новым и старым потоком
                cashflow_diff = newform.cashflow - last_cashflow
                # Исправляю остаток
                newform.balance = newform.balance + cashflow_diff
                # Пересчитываю все остальные потоки исправляя остатки
                change_cashflows_balance(cash)
            # Если тип предыдущего потока "Яндекс деньги"
            elif last_type == 'YANDEX':
                # Исправляю баланс яндекса
                balance.yandex -= last_cashflow
            # Если тип предыдущего потока "Яндекс деньги"
            elif last_type == 'WEBMONEY':
                # Исправляю баланс вебмани
                balance.webmoney -= last_cashflow
            # Если тип нового потока "Наличные"
            if newform.type == 'ENCASH':
                # Исправляю баланс наличных
                balance.encash += newform.cashflow
                # Если предыдущий тип не был "наличные"(иначе все уже исправлено)
                if not last_type == newform.type:
                    # Исправляю остаток
                    newform.balance = newform.cashflow + newform.balance
                    # Пересчитываю все остальные потоки исправляя остатки
                    change_cashflows_balance(cash)
            # Если тип нового потока "Яндекс деньги"
            elif newform.type == 'YANDEX':
                # Исправляю баланс яндекс
                balance.yandex += newform.cashflow
            # Если тип нового потока "Вебмани"
            elif newform.type == 'WEBMONEY':
                # Исправляю баланс вебмани
                balance.webmoney += newform.cashflow
            # Пересчитываю общий баланс
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()
        # Если просто изменился тип потока
        elif not last_type == newform.type:
            balance = Balance.objects.get(id=1)
            # Если предыдущий тип Наличные
            if last_type == 'ENCASH':
                # Изменяю баланс наличных
                balance.encash -= last_cashflow
                # Изменяю остаток
                newform.balance = newform.balance - newform.cashflow
                # Пересчитываю все остальные потоки исправляя остатки
                change_cashflows_balance(cash)
            # Если предыдущий тип яндекс
            elif last_type == 'YANDEX':
                # Изменяю баланс яндекса
                balance.yandex -= last_cashflow
            # Если предыдущий тип вебмани
            elif last_type == 'WEBMONEY':
                # Изменяю баланс вебмани
                balance.webmoney -= last_cashflow
            # Если новый тип наличные
            if newform.type == 'ENCASH':
                # Исправляю баланс наличных
                balance.encash += newform.cashflow
                newform.balance = newform.cashflow + newform.balance
                # Если предыдущий тип не был "наличные"(иначе все уже исправлено)
                if not last_type == newform.type:
                    # Исправляю остаток в других потоках
                    change_cashflows_balance(cash)
            # Если новый тип яндекс
            elif newform.type == 'YANDEX':
                # Исправляю баланс яндекса
                balance.yandex += newform.cashflow
            # Если новый тип вебмани
            elif newform.type == 'WEBMONEY':
                # Исправляю баланс вебмани
                balance.webmoney += newform.cashflow
            # Исправляю весь баланс
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()
        newform.save()

# Изменяет баланс
def change_balance(form):
    balance = Balance.objects.get(id=1)
    if form.cleaned_data['from_type'] == 'ENCASH':
        balance.encash -= form.cleaned_data['amount']
        last_balance = Cash.objects.all().latest('id')
        cash = Cash()
        cash.cashflow = -form.cleaned_data['amount']
        cash.balance = last_balance.balance - form.cleaned_data['amount']
        cash.cause = "OTHER"
        cash.type = "ENCASH"
        if form.cleaned_data['to_type'] == 'YANDEX':
            cash.comment = "На яндекс деньги"
        elif form.cleaned_data['to_type'] == 'WEBMONEY':
            cash.comment = "На webmoney"
    elif form.cleaned_data['from_type'] == 'YANDEX':
        balance.yandex -= form.cleaned_data['amount']
    elif form.cleaned_data['from_type'] == 'WEBMONEY':
        balance.webmoney -= form.cleaned_data['amount']
    if form.cleaned_data['to_type'] == 'ENCASH':
        balance.encash += form.cleaned_data['amount']
    elif form.cleaned_data['to_type'] == 'YANDEX':
        balance.yandex += form.cleaned_data['amount']
        cash.save()
    elif form.cleaned_data['to_type'] == 'WEBMONEY':
        balance.webmoney += form.cleaned_data['amount']
        cash.save()
    balance.total = balance.encash + balance.webmoney + balance.yandex
    balance.save()

def update_cash2(client, client_status):
    # Если статус деньги внесены
    if client.status == 'CASH_IN':
        # Если предыдущий статус такой же, то ничего не делать
        if client_status == client.status:
            pass
        # Если предыдущий статус был другой
        else:
            # Создаю денежный поток
            newcashflow = Cash()
            # Последний баланс
            last_balance = Cash.objects.all().latest('id')
            # Если доставка EMS
            if client.delivery == 'EMS':
                # Добавляю к стоимости 300 рублей
                newcashflow.cashflow = client.subtotal + EMS
                newcashflow.balance = last_balance.balance + client.subtotal + EMS
                newcashflow.comment = client.id
            # Если доставка курьером
            elif client.delivery == 'COURIER':
                # Вычитаю из стоимости 300 рублей
                newcashflow.cashflow = client.subtotal - COURIER
                newcashflow.balance = last_balance.balance + client.subtotal - COURIER
                newcashflow.comment = client.id
            else:
                # Бесплатная доставка
                newcashflow.cashflow = client.subtotal
                newcashflow.balance = last_balance.balance + client.subtotal
                newcashflow.comment = client.id
            newcashflow.cause = 'FROM_CLIENT'
            newcashflow.type = 'ENCASH'
            newcashflow.save()
            balance = Balance.objects.get(id=1)
            balance.encash += newcashflow.cashflow
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()
    else:
        # Если был изменен статус деньги внесены
        if client_status == 'CASH_IN':
            # Удаляю денежный поток и пересчитываю баланс
            cashflow = Cash.objects.get(comment=client.id)
            cashflows_recalc = Cash.objects.filter(pk__gt=cashflow.id).reverse()
            true_balance = cashflow.balance - cashflow.cashflow
            cashflow.delete()
            for cashflow_recalc in cashflows_recalc:
                cashflow_recalc.balance = true_balance + cashflow_recalc.cashflow
                true_balance = cashflow_recalc.balance
                cashflow_recalc.save()
            balance = Balance.objects.get(id=1)
            balance.encash -= cashflow.cashflow
            balance.total = balance.encash + balance.webmoney + balance.yandex
            balance.save()
