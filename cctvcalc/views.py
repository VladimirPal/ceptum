        # -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from cctvcalc.models import Camera

def calc(request):
    return render_to_response("calc/calc.html", locals(), context_instance=RequestContext(request))

def ajx_api(request):
    print request.POST
    cams = Camera.objects.filter(type=request.POST['type'], location=request.POST['location'])
    count_all = len(cams)
    count = 0
    res = str()
    for cam in cams:
        count += 1
        if count == count_all:
            res += cam.resolution
        else:
            res += cam.resolution + ','
    print res
    message = {
        "resolution": res,
        }
    return HttpResponse(message,mimetype='application/json')

