from django.shortcuts import render
# Функции = контроллеры

def index(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/index.html')

def about(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/about.html')

def links(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/links.html')

def contact(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/contacts.html')