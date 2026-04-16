from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .models import Blog, Comment
from .forms import PoolForm, CommentForm, BlogForm

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

def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()
    
    return render(request, 'Auto_DjangoWeb_IvanovLev/registration.html', {'regform': regform})

def blog(request):
    posts = Blog.objects.all()
    return render(request, 'Auto_DjangoWeb_IvanovLev/blog.html', {
        'title': 'Блог',
        'posts': posts,
    })

def blogpost(request, parametr):
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(request, 'Auto_DjangoWeb_IvanovLev/blogpost.html', {
        'post_1': post_1,
        'comments': comments,
        'form': form,
    })

def newpost(request):
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(request, 'Auto_DjangoWeb_IvanovLev/newpost.html', {'blogform': blogform})

def videopost(request):
    return render(request, 'Auto_DjangoWeb_IvanovLev/videopost.html', {'title': 'Видео'})