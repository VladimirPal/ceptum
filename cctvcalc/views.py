        # -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from cctvcalc.models import Camera, Result
import simplejson as json

def calc(request):
    return render_to_response("calc/calc.html", locals(), context_instance=RequestContext(request))

def ajx_api(request):
    print request.POST
    cams = Camera.objects.filter(type=request.POST['type'], camera_class=request.POST['class'], location=request.POST['location'], color=request.POST['color'])
    count_all = len(cams)
    count = 0
    res = str()
    for cam in cams:
        count += 1
        if count == count_all:
            res += cam.resolution
        else:
            res += cam.resolution + ','
    message = {
        "resolution": res,
        }
    print message
    return HttpResponse(json.dumps(message),mimetype='application/json')

def ajx_result(request):
    result = Result(price=0)
    result.save()
    price = 0
    for index, param in enumerate(request.POST.getlist('resolution[]')):
        cam = Camera.objects.get(type=request.POST['type'], camera_class=request.POST['class'],
            location=request.POST.getlist('location[]')[index], resolution=request.POST.getlist('resolution[]')[index],
             color=request.POST.getlist('color[]')[index])
        result.camera.add(cam)
        price += cam.price
    if request.POST.get('m_size', False):
        result.installation = request.POST['m_size']
    result.price = price
    result.save()
    message = {
        "resolution": '/result/%i' % result.id,
        }
    return HttpResponse(json.dumps(message),mimetype='application/json')

def result(request, result_id):
    print result_id
    return render_to_response("calc/result.html", locals(), context_instance=RequestContext(request))

