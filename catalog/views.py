          # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core import urlresolvers
from django.template import RequestContext
from catalog.models import Category, Product, Section
from django.http import HttpResponseRedirect
from cart import cart

def index(request):
    page_title = "Магазин домашней безопасности, шпионская техника"
    meta_keywords = """шпионские штучки магазин, шпионские штучки купить, купить подслушивающее устройство,
     шпионская техника, шпионские камеры, шпионское оборудование продажа, магазин шпионских товаров"""
    meta_description = """Интернет магазин, где можно купить шпионские штучки, камеры,
     подслушивающие устройства. Так же у нас в продаже шпионская техника, оборудование,
      глушилка мобильных телефонов, мини камера."""
    sections = Section.objects.all()
    return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def cats(request):
    cats = Category.objects.all().order_by('id')
    sections = Section.objects.all()
    return render_to_response("main/cats.html", locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    if request.method == 'POST':
        cart.add_to_cart(request)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    else:
        try:
            category = Category.objects.get(slug=category_slug)
            products = category.product_set.filter(is_active=True)
            if category.section.name == category.name:
                page_title = "%s" % category.section
            else:
                page_title = "%s %s" % (category.section, category)
            meta_keywords = category.meta_keywords
            meta_description = category.meta_descriotion
        except :
            section = Section.objects.get(slug=category_slug)
            category = section.category_set.filter(is_active=True)
            page_title = "%s" % section
            products = []
            for cat in category:
                products += cat.product_set.filter(is_active=True)
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def show_section(request, section_slug):
    section = Section.objects.get(slug=section_slug)
    cats = section.category_set.all()
    return render_to_response("main/section.html", locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    photos = product.productphoto_set.all()
    features = product.feature_set.all()
    if request.method == 'POST':
        postdata = request.POST.copy()
        if 'product_slug' in postdata:
            cart.add_to_cart(request)
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    page_title = "%s" % product.name
    meta_keywords = page_title
    meta_description = "%s - %s" % (page_title, product.mini_html_description)
    return render_to_response("main/tovar.html", locals(), context_instance=RequestContext(request))

def all_goods(request):
    if request.method == 'POST':
        cart.add_to_cart(request)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    products = Product.objects.filter(is_active=True)
    page_title = "my-SPY - Все товары"
    meta_keywords = page_title
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def about(request):
    page_title = "О нас"
    return render_to_response('main/about.html', locals(), context_instance=RequestContext(request))

def delivery(request):
    page_title = "Доставка и оплата"
    return render_to_response('main/delivery.html', locals(), context_instance=RequestContext(request))

def internal_error(request):
    return render_to_response('500.html', locals(), context_instance=RequestContext(request))
