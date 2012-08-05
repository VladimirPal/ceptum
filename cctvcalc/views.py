        # -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from cctvcalc.models import Camera

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
    return HttpResponse(message,mimetype='application/json')
