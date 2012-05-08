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
    if request.method == 'POST':
        postdata = request.POST
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.POST['user'])
            client = Client()
            client.name = request.POST['name']
            client.contact_name = request.POST['contact_name']
            client.email = request.POST['email']
            client.status = request.POST['status']
            if postdata.get('status_time', False):
                client.status_time = postdata.get('status_time')
            client.data = request.POST['data']
            client.user = user
            client.save()
        else:
            print "form is not valid"
    else:
          form = ClientForm()
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
