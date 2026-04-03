from django.shortcuts import render
from .forms import PoolForm
# Функции = контроллеры

def index(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/index.html')

def about(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/about.html')

def links(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/links.html')

def contact(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/contacts.html')

def pool(request):
    data = None
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form = None
    else:
        form = PoolForm()
    
    return render(request, 'Auto_DjangoWeb_IvanovLev/pool.html', {'form': form, 'data': data})