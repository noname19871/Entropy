from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from . import russian_news_classifier


def index(request):
    return render(request,'index.html')

def stats(request):
    return render(request,'stats.html')

def about(request):
    return render(request,'about.html')

def swion(request):
    return render(request,'swion.html')

def model(request):
    return render(request,'model.html')

def test(request):
    return render(request,'test.html')

def get_data(request):
    if 'data' in request.GET:
        message = request.GET['data']
        res = russian_news_classifier.predict([message])
    else:
        res = 'You submitted nothing!'

    return HttpResponse(res)