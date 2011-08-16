          # -*- coding: utf-8 -*-
from datetime import date, timedelta
from django.shortcuts import render_to_response
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from cart.models import Client, CartItem, CartProduct
from forms import ClientForm, BaseProductFormset, CashForm, BalanceForm, TaskForm, TaskAnswerForm, OrderForm
from django.forms.models import inlineformset_factory
from cart.cart import _generate_cart_id
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from catalog.models import Product, Category
from models import Cash, Balance, Waytmoney, Task, TaskAnswer, TaskFile, Order, Product_statistic, Cash_statistic
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from madmin_func import clients_list, client_sms, update_store, subtotal, update_cash, update_cash2, cash_list, change_cashflow, change_balance
from django.db.models import Q
from settings import *

def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect("/myadmin/sales/")
        else:
            error = True
    return render_to_response("myadmin/auth.html", locals(), context_instance=RequestContext(request))

@login_required
def logout_view(request):
    logout(request)
    url = urlresolvers.reverse('auth-page')
    return HttpResponseRedirect(url)

def week_boundaries(year, week):
    start_of_year = date(year, 1, 1)
    now = start_of_year + timedelta(weeks=week)
    mon = now - timedelta(days=now.weekday())
    sun = mon + timedelta(days=6)
    return mon, sun

@login_required
def sales(request, when):
    # Ожидаемое количество денег
    money = Waytmoney.objects.get(id=1).wayt_money
    # Список клиентов за запрошеный период
    clients = clients_list(when)
    # Пейджинация
#    try:
#        page = int(request.GET.get('page', '1'))
#    except ValueError:
#        page = 1
    # 100 клиентов на одну страницу
#    paginator = Paginator(clients, 100)
#    try:
#        clients = paginator.page(page)
#    except (EmptyPage, InvalidPage) :
#        clients = paginator.page(paginator.num_pages)
    return render_to_response("myadmin/sale/test.html", locals(), context_instance=RequestContext(request))

@login_required
def sales_active(request):
    # Применяю фильтр по статусам
    if request.method == 'POST':
        # Выбранные статусы
        statuses = []
        # Клиенты соответсвующие статусам
        clients = []
        for status in request.POST.getlist('status'):
            statuses.append(status)
            clients += Client.objects.filter(status=status)
        # Сортирую по id - так чтобы последний клиент был сверху
        clients.sort(key=lambda x: x.id, reverse=True)
    else:
        clients = Client.objects.filter(Q(status="PROCESS") | Q(status="POSTSEND") | Q(status="COURIER_SEND") | Q(status="BACK") | Q(status="CONTACT_AT"))
        statuses = [u'PROCESS',u'POSTSEND',u'COURIER_SEND',u'BACK',u'CONTACT_AT']
    return render_to_response("myadmin/sale/test.html", locals(), context_instance=RequestContext(request))

@login_required
def add_client(request):
    # Создаю формы
    form = ClientForm()
    CartProductFormset = inlineformset_factory(CartItem, CartProduct, formset=BaseProductFormset, extra=1)
    formset = CartProductFormset()
    if request.method == 'POST':
        # Создаю объект корзины для клиента
        cart = CartItem()
        cart.cart_id = _generate_cart_id()
        cart.save()
        # Создаю объект клиента
        client = Client()
        # Сохраняю форму используя объект созданного клиента
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            newform = form.save(commit=False)
            # Записываю корзину клиента
            newform.cart_id = cart.id
            newform.last_user = request.user.first_name
            newform.save()
            # Сохраняю форму используя объект корзины клиента
            formset = CartProductFormset(request.POST, instance=cart)
            if formset.is_valid():
                # Обновляю количество товара на складе
                for formitem in formset.cleaned_data:
                    if formitem:
                        product_name = formitem['product']
                        quantity = formitem['quantity']
                        product = Product.objects.get(name=product_name)
                        true_quantity = product.quantity - quantity
                        product.quantity = true_quantity
                        product.save()
                formset.save()
                # Высчитываю сумму и скидку
                subtotal(cart.id)
            else:
                pass
            # После создания клиента тут же перекидываю на редактирование клиента
            # return HttpResponseRedirect(reverse('myadmin.views.edit_client', args=(client.id,)))
            return HttpResponse(client.id)
    return render_to_response("myadmin/sale/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def delete_client(request, id):
    # УДаляю клиента
    client = Client.objects.get(id=id)
    cart_id = client.cart.id
    client.delete()
    # Уляляю корзину клиента
    cart = CartItem.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect('/myadmin/sales/all')

@login_required
def copy_client(request, id):
    form = ClientForm()
    client = Client.objects.get(id=id)
    client.subtotal = client.discount = client.tracking_number = client.status = client.comment = client.ordered_at = client.delivery = client.tracking_status = client.referrer = client.execute_at = client.last_user = client.change_log = None
    form = ClientForm(instance=client)
    CartProductFormset = inlineformset_factory(CartItem, CartProduct, formset=BaseProductFormset, extra=1)
    formset = CartProductFormset()
    if request.method == 'POST':
        # Создаю объект корзины для клиента
        cart = CartItem()
        cart.cart_id = _generate_cart_id()
        cart.save()
        # Создаю объект клиента
        client = Client()
        # Сохраняю форму используя объект созданного клиента
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            newform = form.save(commit=False)
            # Записываю корзину клиента
            newform.cart_id = cart.id
            newform.last_user = request.user.first_name
            newform.save()
            # Сохраняю форму используя объект корзины клиента
            formset = CartProductFormset(request.POST, instance=cart)
            if formset.is_valid():
                # Обновляю количество товара на складе
                for formitem in formset.cleaned_data:
                    if formitem:
                        product_name = formitem['product']
                        quantity = formitem['quantity']
                        product = Product.objects.get(name=product_name)
                        true_quantity = product.quantity - quantity
                        product.quantity = true_quantity
                        product.save()
                formset.save()
                # Высчитываю сумму и скидку
                subtotal(cart.id)
            else:
                pass
            # После создания клиента тут же перекидываю на редактирование клиента
            return HttpResponseRedirect(reverse('myadmin.views.edit_client', args=(client.id,)))
    return render_to_response("myadmin/sale/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_client(request, id):
    # Получаю нужные данные для работы с формами
    client = Client.objects.get(id=id)
    cartid = client.cart.id
    cart = CartItem.objects.get(id=cartid)
    CartProductFormset = inlineformset_factory(CartItem, CartProduct, formset=BaseProductFormset, extra=1)
    if request.method == 'POST':
        # Получаю предыдущие статусы клиента
        client_status = client.status
        sms_status = client.sms_status
        status = client.status
        # Сохраняю форму используя объект клиента
        form = ClientForm(request.POST, instance=client, prefix='client')
        if form.is_valid():
            newform = form.save(commit=False)
            # Если статус клиента "Снятие заявки клиентом"
            if newform.status == 'REFUSED':
                # Если предыдущий статус тоже был REFUSED
                if status == newform.status:
                    status_refused = False
                else:
                    status_refused = True
            else:
                status_refused = False
            # Сохраняю в базе последнего пользователя редактирующего клиента
            newform.last_user = request.user.first_name
            # Отправляю смс клиенту
            if SEND_SMS:
                if newform.sms_status:
                    if not sms_status:
                        client_sms(newform)
            newform.save()
            # Сохраняю форму используя объект корзины клиента
            formset = CartProductFormset(request.POST, instance=cart)
            if formset.is_valid():
                # Получаю список покупок клиента
                products = CartProduct.objects.filter(cartitem=cart)
                # Обновляю количество товара на складе
                update_store(formset.cleaned_data, products, status_refused)
                formset.save()
                # Высчитываю сумму и скидку
                subtotal(cartid)
            # Обновляю баланс
            update_cash(form.cleaned_data, client, client_status)
        else:
            formset = CartProductFormset(instance=cart)
            return render_to_response("myadmin/sale/client_form.html", locals(), context_instance=RequestContext(request))
    # Создаю формы
    CartProductFormset = inlineformset_factory(CartItem, CartProduct, formset=BaseProductFormset, extra=1)
    formset = CartProductFormset(instance=cart)
    client = Client.objects.get(id=id)
    form = ClientForm(instance=client, prefix='client')
    return render_to_response("myadmin/sale/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def store(request):
    products = Product.objects.all().order_by('category')
    money_in_retail = 0
    money_in_wholesale = 0
    for product in products:
        money_in_retail += product.quantity * product.price
        money_in_wholesale += product.quantity * product.wholesale_price
    return render_to_response("myadmin/store/store.html", locals(), context_instance=RequestContext(request))

@login_required
def cash(request, when):
    balance = Balance.objects.get(id=1)
    # Получаю список денежных потоков за запрошенный период времени
    cash = cash_list(when)
    cash_in = 0
    cash_out = 0
    for i in cash:
        if i.cashflow > 0:
            cash_in += i.cashflow
        else:
            cash_out -= i.cashflow
    cash_all = cash_in + cash_out
    return render_to_response("myadmin/cash/cash.html", locals(), context_instance=RequestContext(request))

@login_required
def add_cashflow(request):
    if request.method == 'POST':
        last_balance = Cash.objects.all().latest('id')
        form = CashForm(request.POST)
        newform = form.save(commit=False)
        balance = Balance.objects.get(id=1)
        if newform.type == 'ENCASH':
            balance.encash += newform.cashflow
            newform.balance = last_balance.balance + newform.cashflow
            balance.total = balance.encash + balance.webmoney + balance.yandex
        elif newform.type == 'WEBMONEY':
            balance.webmoney += newform.cashflow
            newform.balance = last_balance.balance
            balance.total = balance.encash + balance.webmoney + balance.yandex
        elif newform.type == 'YANDEX':
            balance.yandex += newform.cashflow
            newform.balance = last_balance.balance
            balance.total = balance.encash + balance.webmoney + balance.yandex
        balance.save()
        newform.save()
    form = CashForm()
    return render_to_response("myadmin/cash/edit_cashflow.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_cashflow(request, id):
    cash = Cash.objects.get(id=id)
    form = CashForm(instance=cash)
    if request.method == 'POST':
        # Изменяю и пересчитываю денежный поток
        change_cashflow(request, cash)
    return render_to_response("myadmin/cash/edit_cashflow.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_balance(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            # Изменяю баланс
            change_balance(form)
    form = BalanceForm()
    return render_to_response("myadmin/cash/edit_balance.html", locals(), context_instance=RequestContext(request))

@login_required
def tasks(request):
    tasks = Task.objects.filter(is_done=False)
    return render_to_response("myadmin/tasks/tasks.html", locals(), context_instance=RequestContext(request))

@login_required
def add_task(request):
    form = TaskForm()
    TaskFileFormset = inlineformset_factory(Task, TaskFile, extra=1)
    task = Task()
    formset = TaskFileFormset()
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            task.user = request.user.username
            task.save()
            formset = TaskFileFormset(request.POST, request.FILES, instance=task)
            if formset.is_valid():
                formset.save()
            url = urlresolvers.reverse('tasks-page')
            mails = []
            for user in task.performers.all().exclude(username=request.user):
                mails.append(user.email)
            if mails:
                send_mail(u'%s добавил задание для вас' % request.user.first_name, 'http://my-spy.ru/myadmin/tasks/%i/' % task.id, 'info@my-spy.ru', mails)
            return HttpResponseRedirect(url)
    return render_to_response("myadmin/tasks/add_task.html", locals(), context_instance=RequestContext(request))

@login_required
def task(request, id):
    task = Task.objects.get(pk=id)
    answers = TaskAnswer.objects.filter(task=task)
    if request.method == 'POST':
        form = TaskAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.task = task
            newform.user = request.user.username
            newform.save()
            mails = []
            for user in task.performers.all().exclude(username=request.user):
                mails.append(user.email)
            if mails:
                send_mail(u'%s добавил ответ в заданиe' % request.user.first_name, 'http://my-spy.ru/myadmin/tasks/%i/' % task.id, 'info@my-spy.ru', mails)
    form = TaskAnswerForm()
    return render_to_response("myadmin/tasks/task.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_task(request, id):
    task = Task.objects.get(pk=id)
    form = TaskForm(instance=task)
    TaskFileFormset = inlineformset_factory(Task, TaskFile, extra=1)
    formset = TaskFileFormset(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
        formset = TaskFileFormset(request.POST, request.FILES, instance=task)
        if formset.is_valid():
            formset.save()
        url = urlresolvers.reverse('tasks-page')
        return HttpResponseRedirect(url)
    return render_to_response("myadmin/tasks/add_task.html", locals(), context_instance=RequestContext(request))

@login_required
def task_done(request, id):
    task = Task.objects.get(pk=id)
    task.is_done = True
    task.save()
    return HttpResponseRedirect(urlresolvers.reverse(tasks))

@login_required
def delete_task(request, id):
    task = Task.objects.get(pk=id)
    task.delete()
    return HttpResponseRedirect(urlresolvers.reverse(tasks))

@login_required
def show_taskdone(request):
    tasks = Task.objects.filter(is_done=True)
    return render_to_response("myadmin/tasks/tasks.html", locals(), context_instance=RequestContext(request))

@login_required
def my_tasks(request):
    tasks = Task.objects.filter(performers=request.user).exclude(is_done=True)
    return render_to_response("myadmin/tasks/tasks.html", locals(), context_instance=RequestContext(request))

@login_required
def myown_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render_to_response("myadmin/tasks/tasks.html", locals(), context_instance=RequestContext(request))

@login_required
def orders(request):
    orders = Order.objects.all().exclude(is_done=True)
    return render_to_response("myadmin/orders/orders.html", locals(), context_instance=RequestContext(request))

@login_required
def add_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = request.user
            newform.save()
            users = User.objects.all().exclude(username=request.user)
            mails = []
            for user in users:
                mails.append(user.email)
            send_mail(u'%s добавил заказ' % request.user.first_name, 'http://my-spy.ru/myadmin/orders/%i/' % newform.id, 'info@my-spy.ru', mails)
            return HttpResponseRedirect(urlresolvers.reverse(orders))
    return render_to_response("myadmin/orders/order_form.html", locals(), context_instance=RequestContext(request))

@login_required
def order(request, id):
    order = Order.objects.get(id=id)
    return render_to_response("myadmin/orders/order.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_order(request, id):
    order = Order.objects.get(pk=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(urlresolvers.reverse(orders))
    return render_to_response("myadmin/orders/order_form.html", locals(), context_instance=RequestContext(request))

@login_required
def show_orderdone(request):
    orders = Order.objects.filter(is_done=True)
    return render_to_response("myadmin/orders/orders.html", locals(), context_instance=RequestContext(request))

@login_required
def delete_order(request, id):
    order = Order.objects.get(pk=id)
    order.delete()
    return HttpResponseRedirect(urlresolvers.reverse(orders))

@login_required
def order_done(request, id):
    order = Order.objects.get(pk=id)
    order.is_done = True
    order.save()
    return HttpResponseRedirect(urlresolvers.reverse(orders))

@login_required
def statistic(request):
    today = date.today()
    all_profit = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='FROM_CLIENT')))
    all_costs = sum(map(lambda x: x.cash, Cash_statistic.objects.exclude(type='FROM_CLIENT')))
    all_sendgoods = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SENDGOODS')))
    all_purchases = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='PURCHASE')))
    all_bribes = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='BRIBE')))
    all_yandex = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='Yandex')))
    all_phones = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='PHONE')))
    all_others = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='OTHER')))
    all_vladimir = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_VLADIMIR')))
    all_victor = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_VICTOR')))
    all_courier = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_COURIER')))
    all_clean_profit = all_profit - all_costs

    month_profit = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='FROM_CLIENT',date__year=today.year, date__month=today.month)))
    month_costs = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(date__year=today.year, date__month=today.month).exclude(type='FROM_CLIENT')))
    month_sendgoods = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SENDGOODS',date__year=today.year, date__month=today.month)))
    month_purchases = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='PURCHASE',date__year=today.year, date__month=today.month)))
    month_bribes = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='BRIBE',date__year=today.year, date__month=today.month)))
    month_yandex = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='Yandex',date__year=today.year, date__month=today.month)))
    month_phones = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='PHONE',date__year=today.year, date__month=today.month)))
    month_others = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='OTHER',date__year=today.year, date__month=today.month)))
    month_vladimir = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_VLADIMIR',date__year=today.year, date__month=today.month)))
    month_victor = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_VICTOR',date__year=today.year, date__month=today.month)))
    month_courier = sum(map(lambda x: x.cash, Cash_statistic.objects.filter(type='SALARY_COURIER',date__year=today.year, date__month=today.month)))

    products_statistic = Product_statistic.objects.all()

    products = []
    for statistic_item in products_statistic:
        ooo = False
        for product in products:
            # Если такой товар уже есть в списке
            if product.product == statistic_item.product:
                ooo =  True
        # Если товара нету в списке то считаю его
        if not ooo:
                all = products_statistic.filter(product=statistic_item.product)
                new_product = Product_statistic()
                new_product.product = statistic_item.product
                new_product.quantity = 0
                new_product.cash = 0
                for u in all:
                    new_product.quantity += u.quantity
                    new_product.cash += u.cash
                products.append(new_product)
    products.sort(key=lambda x: x.cash, reverse=True)

    last_cat_id = Category.objects.all().latest('id').id

    q = []

    for i in range(1,last_cat_id):
        cash = 0
        cats = Product_statistic.objects.filter(product__category=i)
        for x in cats:
            cash += x.cash
        q.append([x.product.category.all()[0],cash])
    q.sort(key=lambda x: x[1], reverse=True)
    return render_to_response("myadmin/statistic/statistic.html", locals(), context_instance=RequestContext(request))


def test_json(request):
    if request.method == 'POST':
        param = request.POST['param']
        client_id = param.split('.')[0]
        status = param.split('.')[1]
        client = Client.objects.get(id=client_id)
        last_status = client.status
        client.status = status
        client.save()
        update_cash2(client, last_status)
        return HttpResponse(status=200)

def get_client(request, id):
    client = Client.objects.get(id=id)
    return render_to_response("myadmin/sale/client.html", locals(), context_instance=RequestContext(request))
