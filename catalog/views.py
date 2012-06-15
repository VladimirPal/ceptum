          # -*- coding: utf-8 -*-
import re
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.core import urlresolvers
from django.template import RequestContext
from catalog.models import Category, Product, Section, TYPE_CHOICES, LENS_CHOICES, IR_CHOICES, RESOLUTION_CHOICES, SENSIVITY_CHOICES, CameraProduct
from django.http import HttpResponseRedirect, HttpResponse
from cart import cart
import threading
from django.core.mail import send_mail
from cart import settings

def index(request):
    page_title = u'Монтаж видеонаблюдения, установка видеонаблюдения - Цептум. Москва'
    meta_keywords = """установка систем видеонаблюдения монтаж камер лицензия сигнализация прайс
     лист стоимость услуги в квартира офис школа помещение"""
    meta_description = """Все для Видеонаблюдения - установка и монтаж систем видеонаблюдени.
     Продажа видеокамер, видеорегистраторов и аксессуаров по доступным ценам"""
    #sections = Section.objects.filter(is_active=True)
    return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def video_solutions(request):
    page_title = u'Типовые решения - Цептум. Москва'
    return render_to_response('main/solutions/index.html', locals(), context_instance=RequestContext(request))

def cats(request):
    cats = Category.objects.all()
    sections = Section.objects.all()
    return render_to_response("main/cats.html", locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    if (category_slug == 'street-analog') or (category_slug == 'domical-analog') or (category_slug == 'mini-analog'):
        filter = True
        type_choices = TYPE_CHOICES
        lens_choices = LENS_CHOICES
        ir_choices = IR_CHOICES
        resolution_choices = RESOLUTION_CHOICES
        sensevity_choices = SENSIVITY_CHOICES
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        if 'product_slug' in request.POST:
            cart.add_to_cart(request)
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
        else:
            options = request.POST.getlist('option')
            for option in options:
                features_dict2 = {}
                category = Category.objects.get(slug=category_slug)
                for option in request.POST.getlist('option'):
                    values = features_dict2.get(option.split(':')[0], [])
                    try:
                        if option.split(':')[1] not in features_dict2[option.split(':')[0]]:
                            features_dict2[option.split(':')[0]] = values + [option.split(':')[1]]
                    except:
                        features_dict2[option.split(':')[0]] = values + [option.split(':')[1]]
                kwargs = {}
                counter = 0
                args = Q()
                for name, values in features_dict2.items():
                    if name == 'resolution':
                        args &= ( Q( resolution1__in = values ) | Q( resolution2__in = values ) )
                    elif name == 'sensitivity':
                        args &= ( Q( sensitivity1__in = values ) | Q( sensitivity2__in = values ) )
                    elif (name == 'type') and ('color' in values):
                        for value in values:
                            if value == 'color':
                                args &= ( Q( type = value ) | Q( type = 'day-night' ) )
                            else:
                                kwargs[str(name) + '__in'] = values
                    else:
                        kwargs[str(name) + '__in'] = values
                products = CameraProduct.objects.filter(category=category).filter(args,**kwargs)
            if not options:
                products = category.product_set.filter(is_active=True).order_by('categoryproduct__position')
    else:
        products = category.product_set.filter(is_active=True).order_by('categoryproduct__position')
    if category.section.name == category.name:
        page_title = u'%s - Цептум' % category.section
    else:
        page_title = u'%s %s - Цептум' % (category.section, category)
    meta_keywords = category.meta_keywords
    meta_description = category.meta_descriotion
    sections = Section.objects.filter(is_active=True)
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))


def show_section(request, section_slug):
    section = get_object_or_404(Section, slug=section_slug)
    sections = Section.objects.filter(is_active=True)
    cats = section.category_set.filter(is_active=True)
    page_title = section.name + u' - Цептум'
    return render_to_response("main/section.html", locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    photos = product.productphoto_set.all()
    if request.method == 'POST':
        postdata = request.POST.copy()
        if 'product_slug' in postdata:
            cart.add_to_cart(request)
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    page_title = u'%s - Цептум' % product.name
    meta_keywords = page_title
    meta_description = "%s - %s" % (page_title, product.mini_html_description)
    sections = Section.objects.filter(is_active=True)
    return render_to_response("main/tovar.html", locals(), context_instance=RequestContext(request))

def all_goods(request):
    if request.method == 'POST':
        cart.add_to_cart(request)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    products = Product.objects.filter(is_active=True)
    page_title = u'Цептум Все товары'
    meta_keywords = page_title
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def about(request):
    page_title = u'Контакты - Цептум. Москва'
    return render_to_response('main/about.html', locals(), context_instance=RequestContext(request))

def install(request):
    page_title = u'Услуги по установке видеонаблюдения - Цептум. Москва'
    return render_to_response('main/install.html', locals(), context_instance=RequestContext(request))

def service(request):
    page_title = u'Обслуживание систем видеонаблюдения - Цептум. Москва'
    return render_to_response('main/service.html', locals(), context_instance=RequestContext(request))

def internal_error(request):
    return render_to_response('500.html', locals(), context_instance=RequestContext(request))

def take_call_form(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if not "href" in postdata['message']:
            if settings.SEND_ADMIN_EMAIL:
                t = threading.Thread(target= send_mail, args=[
                    u'Перезвонить, %s' % postdata['name'],
                    u'Имя: %s \nТелефон: %s\nСообщение: %s\n' % (postdata['name'], postdata['phone'], postdata['message']),
                   settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
                t.setDaemon(True)
                t.start()
        return HttpResponse()

def take_vk_comment(request):
    if request.method == 'POST':
        param = request.POST['comment']
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
            u'Новый комментарий',
            u'%s' % param, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
    return HttpResponse()

def office(request):
    page_title = u'Видеонаблюдение в офис - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в офис'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/office.html', locals(), context_instance=RequestContext(request))

def business_center(request):
    page_title = u'Видеонаблюдение в бизнес-центр - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в бизнес-центр'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/business-center.html', locals(), context_instance=RequestContext(request))

def store(request):
    page_title = u'Видеонаблюдение в магазин - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в магазин'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/store.html', locals(), context_instance=RequestContext(request))

def market(request):
    page_title = u'Видеонаблюдение в торговый центр - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в торговый центр'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/market.html', locals(), context_instance=RequestContext(request))

def sklad(request):
    page_title = u'Видеонаблюдение на склад - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение на склад'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/sklad.html', locals(), context_instance=RequestContext(request))

def cafe(request):
    page_title = u'Видеонаблюдение в Кафе/Бар/Ресторан - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в кафе'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/cafe.html', locals(), context_instance=RequestContext(request))

def club(request):
    page_title = u'Видеонаблюдение в Ночной клуб - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в ночной клуб'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/club.html', locals(), context_instance=RequestContext(request))

def podezd(request):
    page_title = u'Видеонаблюдение в подъезд - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в подъезд'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/podezd.html', locals(), context_instance=RequestContext(request))

def cotedge(request):
    page_title = u'Видеонаблюдение в Дом/Коттеджный поселок - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в коттедж'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/cotedge.html', locals(), context_instance=RequestContext(request))

def otel(request):
    page_title = u'Видеонаблюдение в Отель - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в отель'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/otel.html', locals(), context_instance=RequestContext(request))

def beauty(request):
    page_title = u'Видеонаблюдение в Салон красоты - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в салон красоты'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/beauty.html', locals(), context_instance=RequestContext(request))

def fitness(request):
    page_title = u'Видеонаблюдение в Фитнес центр - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в фитнес-центр'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/fitness.html', locals(), context_instance=RequestContext(request))

def autoservice(request):
    page_title = u'Видеонаблюдение в автосервис/автомойка - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в автосервис'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/autoservice.html', locals(), context_instance=RequestContext(request))

def autostore(request):
    page_title = u'Видеонаблюдение в автосалон - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в автосалон'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/autostore.html', locals(), context_instance=RequestContext(request))

def parking(request):
    page_title = u'Видеонаблюдение на парковку - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение на парковку'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/parking.html', locals(), context_instance=RequestContext(request))

def proizvodstvo(request):
    page_title = u'Видеонаблюдение на Производство - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение на производство'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/proizvodstvo.html', locals(), context_instance=RequestContext(request))

def social(request):
    page_title = u'Видеонаблюдение в социальное учреждение - Цептум. Москва'
    if request.method == 'POST':
        postdata = request.POST
        if not postdata.get('product_slug', ''):
            product_slug = u'Видеонаблюдение в социальное учреждение'
        else:
            product_slug = postdata.get('product_slug','')
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
                u'Заказ на %s' % product_slug,
                u'Имя: %s \nТелефон: %s\nЗаказ: %s\nСообщение: %s\nАдрес: %s\nEmail: %s\n' % (postdata['name'], postdata['phone'], product_slug, postdata['comment'], postdata['address'], postdata['email']),
                settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
        return HttpResponse()
    return render_to_response('main/solutions/social.html', locals(), context_instance=RequestContext(request))
