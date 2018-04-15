from django.http import HttpResponse
from django.shortcuts import render


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

def change_view(request):
    return request.data[text]