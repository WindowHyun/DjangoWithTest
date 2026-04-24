from django.http import HttpResponse
from django.shortcuts import render

# https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")