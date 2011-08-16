from datetime import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Entry, Category

def blog(request):
    first_entry = Entry.objects.order_by()[0].date
    entrys = Entry.objects.filter(date__range=(first_entry, datetime.now()))
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(entrys, 15)
    try:
        entrys = paginator.page(page)
    except (EmptyPage, InvalidPage) :
        entrys = paginator.page(paginator.num_pages)
    return render_to_response("blog/main.html", locals(), context_instance=RequestContext(request))

def archive(request, when):
    entrys = Entry.objects.filter(date__year=when[-4:], date__month=when[:-4])
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(entrys, 15)
    try:
        entrys = paginator.page(page)
    except (EmptyPage, InvalidPage) :
        entrys = paginator.page(paginator.num_pages)
    return render_to_response("blog/main.html", locals(), context_instance=RequestContext(request))

def entry(request, entry_slug):
    entry = Entry.objects.get(slug=entry_slug)
    return render_to_response("blog/entry.html", locals(), context_instance=RequestContext(request))

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    entrys = Entry.objects.filter(category=category)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(entrys, 15)
    try:
        entrys = paginator.page(page)
    except (EmptyPage, InvalidPage) :
        entrys = paginator.page(paginator.num_pages)
    return render_to_response("blog/main.html", locals(), context_instance=RequestContext(request))
