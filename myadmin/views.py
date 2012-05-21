          # -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category, Section
from django.contrib.auth import logout
from models import Client, Comment, CommentFile
from django.contrib.auth.models import User
from myadmin.forms import myClientForm, CommentForm, TargetForm
from myadmin.models import ClientFile
from django.forms.models import inlineformset_factory
from myadmin.models import STATUS_CHOICES
import datetime
from myadmin.models import CategoryTarget, Target
from django.shortcuts import redirect

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
        if request.GET.get('time',''):
            time = request.GET.get('time')
            if time == 'today':
                clients = Client.objects.filter(user=user, status__in=current_statuses, status_date=datetime.date.today()).exclude(status_date__isnull=True).order_by('status_date')
        else:
            clients = Client.objects.filter(user=user, status__in=current_statuses).order_by('status_date')
    except :
        clients = False
    expired_count = Client.objects.filter(user=user).exclude(status_date__gte=datetime.date.today()).exclude(status_date__isnull=True).count()
    today_count = Client.objects.filter(user=user, status_date=datetime.date.today()).count()
    status_statistic = {}
    for status, y in STATUS_CHOICES:
        status_statistic[y] = Client.objects.filter(user=user, status=status).count()
    return render_to_response("myadmin/clients/index.html", locals(), context_instance=RequestContext(request))

@login_required
def user_clients(request, username):
    if request.GET.getlist('status'):
        current_statuses = []
        for status in request.GET.getlist('status'):
            current_statuses.append(status)
    else:
        current_statuses = dict((x) for x in STATUS_CHOICES)
        del current_statuses['DONE']
    statuses = STATUS_CHOICES
    user = User.objects.get(username=username)
    clientsuser = user.get_full_name()
    try:
        if request.GET.get('time',''):
            time = request.GET.get('time')
            if time == 'today':
                clients = Client.objects.filter(user=user, status__in=current_statuses, status_date=datetime.date.today()).exclude(status_date__isnull=True).order_by('status_date')
        elif request.GET.get('expired', ''):
            clients = Client.objects.filter(user=user).exclude(status_date__gte=datetime.date.today()).exclude(status_date__isnull=True).order_by('status_date')
        else:
            clients = Client.objects.filter(user=user, status__in=current_statuses).order_by('status_date')
    except :
        clients = False
    expired_count = Client.objects.filter(user=user).exclude(status_date__gte=datetime.date.today()).exclude(status_date__isnull=True).count()
    today_count = Client.objects.filter(user=user, status_date=datetime.date.today()).count()
    status_statistic = {}
    for status, y in STATUS_CHOICES:
        status_statistic[y] = Client.objects.filter(user=user, status=status).count()
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
        if request.GET.get('time',''):
            time = request.GET.get('time')
            if time == 'today':
                clients = Client.objects.filter(status__in=current_statuses, status_date=datetime.date.today()).order_by('status_date')
        elif request.GET.get('expired', ''):
            clients = Client.objects.exclude(status_date__gte=datetime.date.today()).exclude(status_date__isnull=True).order_by('status_date')
        else:
            clients = Client.objects.filter(status__in=current_statuses).order_by('status_date')
    except :
        clients = False
    expired_count = Client.objects.exclude(status_date__gte=datetime.date.today()).exclude(status_date__isnull=True).count()
    today_count = Client.objects.filter(status_date=datetime.date.today()).count()
    status_statistic = {}
    for status, y in STATUS_CHOICES:
        status_statistic[y] = Client.objects.filter(status=status).count()
    return render_to_response("myadmin/clients/index.html", locals(), context_instance=RequestContext(request))

@login_required
def add_client(request):
    form = myClientForm(exclude_list=('profit',),initial={'user': request.user.id})
    FileFormset = inlineformset_factory(Client, ClientFile, extra=2)
    client = Client()
    formset = FileFormset()
    if request.method == 'POST':
        form = myClientForm((),request.POST, instance=client)
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
    form = myClientForm(exclude_list=('referrer',), instance=client)
    FileFormset = inlineformset_factory(Client, ClientFile, extra=1)
    formset = FileFormset(instance=client)
    if request.method == 'POST':
        form = myClientForm(('referrer',), request.POST, instance=client)
        if form.is_valid():
            form.save()
            formset = FileFormset(request.POST, request.FILES, instance=client)
            if formset.is_valid():
                formset.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                ref = request.session.get('ref')
                if ref:
                    return redirect(ref)
                else:
                    return redirect('/myadmin/clients')
    else:
        request.session['ref'] = request.META.get('HTTP_REFERER')
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))

@login_required
def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return HttpResponseRedirect(urlresolvers.reverse('clients'))

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

@login_required
def client_page(request, id):
    client = Client.objects.get(id=id)
    user = User.objects.get(username=request.user)
    comment = Comment()
    form = CommentForm()
    FileFormset = inlineformset_factory(Comment, CommentFile, extra=1)
    formset = FileFormset()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = user
            newform.client = client
            newform.save()
            formset = FileFormset(request.POST, request.FILES, instance=comment)
            if formset.is_valid():
                formset.save()
    form = CommentForm()
    formset = FileFormset()
    return render_to_response("myadmin/clients/client_page.html", locals(), context_instance=RequestContext(request))

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

@login_required
def cold_choose_cat(request):
    categorys = CategoryTarget.objects.all()
    return render_to_response("myadmin/cold/index.html", locals(), context_instance=RequestContext(request))

@login_required
def cold_start(request, category_id):
    user = User.objects.get(username=request.user)
    if request.session.get('last_target'):
        last_target = Target.objects.get(id=request.session.get('last_target'))
        if not last_target.is_done:
            if not last_target.callback:
                if last_target.is_busy:
                    last_target.is_busy = False
                    last_target.save()
    if request.method == 'POST':
        target = Target.objects.get(id=request.POST.get("target_id"))
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            if target.callback_at:
                target.callback = True
                target.is_busy = True
            else:
                target.is_busy = False
                target.is_done = True
                target.is_positive = False
                target.done_at = datetime.date.today()
            target.user = user
            target.save()
            return HttpResponseRedirect(request.path)
    else:
        category = CategoryTarget.objects.get(id=category_id)
        target = Target.objects.filter(category=category, is_busy=False, is_done=False).order_by('?')[0]
        target.is_busy = True
        target.is_busy_at = datetime.datetime.today()
        target.save()
        form = TargetForm(instance=target)
        request.session['last_target'] = target.id
    return render_to_response("myadmin/cold/start.html", locals(), context_instance=RequestContext(request))

@login_required
def cold_to_client(request):
    target = Target.objects.get(id=request.GET.get('target'))
    contact_name = ''
    for phone in target.phone_set.all():
        contact_name += phone.phone + '\n'
    form = myClientForm(exclude_list=(),initial={'user': request.user.id, 'referrer': 'COLD', 'name': target.name,\
                         'contact_name':contact_name, 'email':target.email, 'address':target.address})
    FileFormset = inlineformset_factory(Client, ClientFile, extra=2)
    client = Client()
    formset = FileFormset()
    if request.method == 'POST':
        form = myClientForm((),request.POST, instance=client)
        if form.is_valid():
            form.save()
            formset = FileFormset(request.POST, request.FILES, instance=client)
            if formset.is_valid():
                formset.save()
            target.is_busy = False
            target.is_done = True
            target.is_positive = True
            target.callback = False
            target.done_at = datetime.date.today()
            target.save()
            return HttpResponseRedirect(urlresolvers.reverse('clients'))
    return render_to_response("myadmin/clients/client_form.html", locals(), context_instance=RequestContext(request))
