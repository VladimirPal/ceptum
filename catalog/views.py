          # -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from ordereddict import OrderedDict
from django.shortcuts import get_object_or_404, render_to_response
from django.core import urlresolvers
from django.template import RequestContext
from catalog.models import Category, Product, Section, TYPE_CHOICES, LENS_CHOICES, IR_CHOICES, RESOLUTION_CHOICES, SENSIVITY_CHOICES, CameraProduct
from django.http import HttpResponseRedirect
from cart import cart

def index(request):
    page_title = "Системы видеонаблюдения"
    meta_keywords = """шпионские штучки магазин, шпионские штучки купить, купить подслушивающее устройство,
     шпионская техника, шпионские камеры, шпионское оборудование продажа, магазин шпионских товаров"""
    meta_description = """Интернет магазин, где можно купить шпионские штучки, камеры,
     подслушивающие устройства. Так же у нас в продаже шпионская техника, оборудование,
      глушилка мобильных телефонов, мини камера."""
    sections = Section.objects.all()
    return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

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
    category = Category.objects.get(slug=category_slug)
#    all_features = Feature.objects.filter(item__category__slug=category_slug)
#    features_dict = OrderedDict()
#    for feature in all_features:
#        values = features_dict.get(feature.name.name, [])
#        try:
#            values.sort()
#        except :
#            pass
#        try:
#            if feature.value.value not in features_dict[feature.name.name]:
#                features_dict[feature.name.name] = values + [feature.value.value]
#        except:
#            features_dict[feature.name.name] = values + [feature.value.value]
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
            page_title = "%s" % category.section
        else:
            page_title = "%s %s" % (category.section, category)
        meta_keywords = category.meta_keywords
        meta_description = category.meta_descriotion
#        except :
#            section = Section.objects.get(slug=category_slug)
#            category = section.category_set.filter(is_active=True)
#            page_title = "%s" % section
#            products = []
#            for cat in category:
#                products += cat.product_set.filter(is_active=True).order_by('categoryproduct__sort_number')
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def show_section(request, section_slug):
    section = Section.objects.get(slug=section_slug)
    cats = section.category_set.filter(is_active=True)
    page_title = section.name
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
    page_title = "%s" % product.name
    meta_keywords = page_title
    meta_description = "%s - %s" % (page_title, product.mini_html_description)
    sections = Section.objects.all()
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
    page_title = "Оплата и Монтаж"
    return render_to_response('main/delivery.html', locals(), context_instance=RequestContext(request))

def internal_error(request):
    return render_to_response('500.html', locals(), context_instance=RequestContext(request))
