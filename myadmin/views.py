          # -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category, Section
from django.contrib.auth import logout
from forms import ClientForm
from models import Client
from django.contrib.auth.models import User

def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            try:
                return HttpResponseRedirect(request.GET['next'])
            except :
                return HttpResponseRedirect(urlresolvers.reverse('clients'))
        else:
            error = True
    return render_to_response("myadmin/auth.html", locals(), context_instance=RequestContext(request))

@login_required
def logout_view(request):
    logout(request)
    url = urlresolvers.reverse('auth-page')
    return HttpResponseRedirect(url)

@login_required
def clients(request):
    user = User.objects.get(username=request.user)
    try:
        clients = Client.objects.filter(user=user)
    except :
        clients = False
    return render_to_response("myadmin/clients/index.html", locals(), context_instance=RequestContext(request))

@login_required
def add_client(request):
    users = User.objects.all()
    if request.method == 'POST':
        postdata = request.POST
        # Validation
        errors = {}
        name = postdata.get('name','')
        contacts = postdata.get('contacts','')
        status = postdata.get('status','')
        manager = postdata.get('manager','')
        if not name:
            errors['name'] = 'Введите название'
        if not contacts:
            errors['contacts'] = 'Введите контактное лицо'
        if not status:
            errors['status'] = 'Укажите статус'
        if not manager:
            errors['manager'] = 'Укажите исполнителя'
        if not errors:
            user = User.objects.get(id=postdata.get('manager'))
            client = Client()
            client.name = name
            client.contact_name = contacts
            client.email = postdata.get('email','')
            client.status = status
            if postdata.get('status_time', False):
                client.status_time = postdata.get('status_time')
            client.data = postdata.get('data','')
            client.user = user
            client.save()
            return HttpResponseRedirect(urlresolvers.reverse('clients'))
        else:
            return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))
    else:
        pass
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def store(request):
    sections = Section.objects.all()
    if request.method == "POST":
        category_select = Category.objects.filter(id__in = request.POST.getlist("category_select"))
        products = Product.objects.filter(category__in = category_select)
        return render_to_response("myadmin/store/store.html", locals(), context_instance=RequestContext(request))
    products = Product.objects.all()
    return render_to_response("myadmin/store/store.html", locals(), context_instance=RequestContext(request))

@login_required
def unstore(request):
    products = Product.objects.filter(quantity=0)
    return render_to_response("myadmin/store/store.html", locals(), context_instance=RequestContext(request))

@login_required
def allstore(request):
    products = Product.objects.all()
    return render_to_response("myadmin/store/store.html", locals(), context_instance=RequestContext(request))

@login_required
def change_product_field(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['id'])
        if request.POST['field'] == 'quantity':
            product.quantity = request.POST['val']
        elif request.POST['field'] == 'price':
            product.price = request.POST['val']
        elif request.POST['field'] == 'wholesale_price':
            product.wholesale_price = request.POST['val']
        product.save()
        return HttpResponse(status=200)
