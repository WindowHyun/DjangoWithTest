from django.http import HttpResponse
from django.shortcuts import render
from .models import Question

# https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

    question_list = Question.objects.order_by('-create_date') # - 붙으면 역순 정렬
    context = {'question_list' : question_list}
    return render(request, 'pybo/question_list.html', context)
    # render : question_list 데이터를 question_list.html에 적용하여 html 생성 후 리턴