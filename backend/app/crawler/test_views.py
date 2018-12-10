from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def page_1(request):
    return render(request, 'page_1.html')


def page_2(request):
    return render(request, 'page_2.html')


def page_3(request):
    return render(request, 'page_3.html')


def page_4(request):
    return render(request, 'page_4.html')
