          # -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from projects.models import Project, Category

def all_projects(request):
    projects = Project.objects.all().order_by("-date")
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(projects, 15)
    try:
        projects = paginator.page(page)
    except (EmptyPage, InvalidPage) :
        projects = paginator.page(paginator.num_pages)
    page_title = "Наши работы"
    return render_to_response("projects/main.html", locals(), context_instance=RequestContext(request))

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    projects = Project.objects.filter(category=category).order_by("-date")
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(projects, 15)
    try:
        projects = paginator.page(page)
    except (EmptyPage, InvalidPage) :
        projects = paginator.page(paginator.num_pages)
    page_title = category.name
    return render_to_response("projects/main.html", locals(), context_instance=RequestContext(request))

def project(request, entry_slug):
    project = Project.objects.get(slug=entry_slug)
    page_title = project.name
    return render_to_response("projects/project.html", locals(), context_instance=RequestContext(request))
