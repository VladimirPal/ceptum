        # -*- coding: utf-8 -*-
from cctvcalc.forms import TypeForm, IpForm, RecorderForm, MicForm, InstallForm, IpCamForm
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from cart.cart import _cart_id
from cctvcalc.models import CalcCart, IpCams
from django.forms.models import modelformset_factory
from django.contrib.formtools.wizard.views import SessionWizardView


class CalcWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        print "lal"

def calc(request):
    return render_to_response("calc/calc.html", locals(), context_instance=RequestContext(request))

def type(request):
    form = TypeForm()
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
    else:
        calccart = CalcCart(calc_id=calc_id).save()
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            system_type = form.cleaned_data['system_type']
            calccart.system_type = system_type
            calccart.save()
            return HttpResponseRedirect(urlresolvers.reverse('ip'))
    return render_to_response("calc/type.html", locals(), context_instance=RequestContext(request))

def ip(request):
    form = IpForm()
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.system_type:
            return HttpResponseRedirect(urlresolvers.reverse('type'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('type'))
    if request.method == 'POST':
        form = IpForm(request.POST)
        if form.is_valid():
            is_ip = int(form.cleaned_data['is_ip'])
            calccart.is_ip = is_ip
            calccart.save()
            if is_ip:
                return HttpResponseRedirect(urlresolvers.reverse('ip-cams'))
    return render_to_response("calc/ip.html", locals(), context_instance=RequestContext(request))

def ipcams(request):
    IpCamsFormset = modelformset_factory(IpCams, form=IpCamForm)
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.is_ip:
            if not calccart.system_type:
                return HttpResponseRedirect(urlresolvers.reverse('type'))
            else:
                return HttpResponseRedirect(urlresolvers.reverse('ip'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('type'))
    formset = IpCamsFormset(initial=[{'cart':calccart}])
    if request.method == 'POST':
        formset = IpCamsFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(urlresolvers.reverse('rec'))
    return render_to_response("calc/ipcams.html", locals(), context_instance=RequestContext(request))

def recorder(request):
    form = RecorderForm()
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.system_type:
            return HttpResponseRedirect(urlresolvers.reverse('type'))
    else:
        calccart = CalcCart(calc_id=calc_id).save()
    if request.method == 'POST':
        form = RecorderForm(request.POST)
        if form.is_valid():
            recorder_time = form.cleaned_data['recorder_time']
            speed_record = form.cleaned_data['speed_record']
            calccart.recorder_time = recorder_time
            calccart.speed_record = speed_record
            calccart.save()
            return HttpResponseRedirect(urlresolvers.reverse('mic'))
    return render_to_response("calc/recorder.html", locals(), context_instance=RequestContext(request))

def mic(request):
    form = MicForm()
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.system_type:
            return HttpResponseRedirect(urlresolvers.reverse('type'))
    else:
        calccart = CalcCart(calc_id=calc_id).save()
    if request.method == 'POST':
        form = MicForm(request.POST)
        if form.is_valid():
            count_microfone = form.cleaned_data['count_microfone']
            calccart.count_microfone = count_microfone
            calccart.save()
            return HttpResponseRedirect(urlresolvers.reverse('install'))
    return render_to_response("calc/recorder.html", locals(), context_instance=RequestContext(request))

def install(request):
    form = InstallForm()
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.system_type:
            return HttpResponseRedirect(urlresolvers.reverse('type'))
    else:
        calccart = CalcCart(calc_id=calc_id).save()
    if request.method == 'POST':
        form = InstallForm(request.POST)
        if form.is_valid():
            cable_length = form.cleaned_data['cable_length']
            calccart.cable_length = cable_length
            calccart.save()
            return HttpResponseRedirect(urlresolvers.reverse('result'))
    return render_to_response("calc/install.html", locals(), context_instance=RequestContext(request))

def result(request):
    calc_id = _cart_id(request)
    if CalcCart.objects.filter(calc_id=calc_id):
        calccart = CalcCart.objects.get(calc_id=calc_id)
        if not calccart.system_type:
            return HttpResponseRedirect(urlresolvers.reverse('type'))
    else:
        calccart = CalcCart(calc_id=calc_id).save()
    return render_to_response("calc/result.html", locals(), context_instance=RequestContext(request))
