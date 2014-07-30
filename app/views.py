from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
# Create your views here.

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )