          # -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category, Section
from django.contrib.auth import logout
from models import Client
from django.contrib.auth.models import User
from myadmin.forms import ClientForm
from myadmin.models import ClientFile
from django.forms.models import inlineformset_factory
from madmin_func import valid_client_form
from myadmin.models import STATUS_CHOICES

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
    if request.GET.getlist('status'):
        current_statuses = []
        for status in request.GET.getlist('status'):
            current_statuses.append(status)
    else:
        current_statuses = dict((x) for x in STATUS_CHOICES)
        del current_statuses['DONE']
    statuses = STATUS_CHOICES
    user = User.objects.get(username=request.user)
    try:
        print current_statuses
        clients = Client.objects.filter(user=user, status__in=current_statuses)
    except :
        clients = False
    return render_to_response("myadmin/clients/index.html", locals(), context_instance=RequestContext(request))

@login_required
def clients_all(request):
    if request.GET.getlist('status'):
        current_statuses = []
        for status in request.GET.getlist('status'):
            current_statuses.append(status)
    else:
        current_statuses = dict((x) for x in STATUS_CHOICES)
        del current_statuses['DONE']
    statuses = STATUS_CHOICES
    try:
        print current_statuses
        clients = Client.objects.filter(status__in=current_statuses)
    except :
        clients = False
    return render_to_response("myadmin/clients/index.html", locals(), context_instance=RequestContext(request))

@login_required
def add_client(request):
    form = ClientForm(initial={'user': request.user.id})
    FileFormset = inlineformset_factory(Client, ClientFile, extra=2)
    client = Client()
    formset = FileFormset()
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            formset = FileFormset(request.POST, request.FILES, instance=client)
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(urlresolvers.reverse('clients'))
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def edit_client(request, id):
    client = Client.objects.get(id=id)
    form = ClientForm(initial={'user': request.user.id}, instance=client)
    FileFormset = inlineformset_factory(Client, ClientFile, extra=1)
    formset = FileFormset(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            formset = FileFormset(request.POST, request.FILES, instance=client)
            if formset.is_valid():
                formset.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                return HttpResponseRedirect(urlresolvers.reverse('clients'))
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return HttpResponseRedirect(urlresolvers.reverse('clients'))

import datetime
@login_required
def edit_ajx_client(request):
    if request.method == 'POST':
        client = Client.objects.get(id=request.POST.get('id',''))
        if request.POST.get('status', False):
            client.status = request.POST.get('status','')
        if 'date' in request.POST:
            if request.POST.get('date',''):
                client.status_date = datetime.datetime.strptime(request.POST.get('date'), '%d.%m.%Y').date()
            else:
                client.status_date = None
        if 'time' in request.POST:
            if request.POST.get('time',''):
                client.status_time = request.POST.get('time','')
            else:
                client.status_time = None
        if request.POST.get('comment', False):
            client.status_comment = request.POST.get('comment','')
        client.save()
        return HttpResponse(status=200)
"""
from myadmin.models import ClientFile
from django.core.files.base import ContentFile
from ceptum.settings import MEDIA_ROOT
import os
@login_required
def add_client(request):
    users = User.objects.all()
    if request.method == 'POST':
        postdata = request.POST
        # Validation
        errors = valid_client_form(postdata)
        if not errors:
            user = User.objects.get(id=postdata.get('user'))
            client = Client()
            client.name = postdata.get('name','')
            client.contact_name = postdata.get('contact_name','')
            client.email = postdata.get('email','')
            client.status = postdata.get('status','')
            if postdata.get('status_time', False):
                client.status_time = postdata.get('status_time')
            client.data = postdata.get('data','')
            client.user = user
            client.save()
            for upfile in request.FILES.getlist('file'):
                FILE_ROOT = os.path.join(MEDIA_ROOT, 'clientfiles')
                myfile = ContentFile(upfile.read())
                myfile.name = os.path.join(FILE_ROOT, upfile.name)
                file_model = ClientFile()
                file_model.file = myfile
                file_model.save()
                client.file.add(file_model)
            client.save()
            return HttpResponseRedirect(urlresolvers.reverse('clients'))
        else:
            return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))
    else:
        pass
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))
"""

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
