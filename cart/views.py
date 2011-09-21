          # -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import OrderForm
from settings import *
import cart

def show_cart(request):
    page_title = 'Корзина'
    is_order = False
    form = OrderForm()
    # Содержимое корзины
    cart_items = cart.get_cart_items(request)
    if request.method == 'POST':
        postdata = request.POST.copy()
        if 'Remove' in postdata:
            cart.remove_from_cart(request)
        elif 'Update' in postdata:
            cart.update_cart(request)
        else:
            form = OrderForm(request.POST)
            if form.is_valid():
                # Пишу клиента в базу
                cart.save_client(request, form)
                is_order = True
    # Высчитывается скидка и общая стоимость
    if cart_items:
        subtotal_class = cart.Subtotal(request)
        cart_subtotal = subtotal_class.subtotal()
        discount = subtotal_class.discount
        # Если заказ сделан
        if is_order:
            # Отправляем админу смс
            if SEND_SMS:
                cart.send_sms(cart_items, form)
            # Отправляем админу email
            if SEND_ADMIN_EMAIL:
                cart.send_admin_email(request, cart_items, form, cart_subtotal, discount)
            # Отправляем email клиенту
            if SEND_CLIENT_EMAIL:
                if form.cleaned_data['email']:
                    cart.send_client_email(cart_items, form, cart_subtotal)
            # Удаляю сессию у клиента
            del request.session['cart_id']
            # Очищаю корзину клиента
            cart_items = False
    return render_to_response("cart/cart.html", locals(), context_instance=RequestContext(request))
