from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Blog, Comment, Category, CatalogItem, Order, OrderItem
from .forms import PoolForm, CommentForm, BlogForm, CategoryForm, CatalogItemForm

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


def catalog(request):
    categories = Category.objects.all()
    return render(request, 'Auto_DjangoWeb_IvanovLev/catalog.html', {'categories': categories})

def category(request, category_id):
    category_obj = Category.objects.get(id=category_id)
    items = CatalogItem.objects.filter(category=category_obj)
    return render(request, 'Auto_DjangoWeb_IvanovLev/category.html', {'category': category_obj, 'items': items})

def catalog_item(request, item_id):
    item = CatalogItem.objects.get(id=item_id)
    return render(request, 'Auto_DjangoWeb_IvanovLev/catalog_item.html', {'item': item})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm()
    return render(request, 'Auto_DjangoWeb_IvanovLev/add_category.html', {'form': form})

def add_catalog_item(request):
    if request.method == 'POST':
        form = CatalogItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CatalogItemForm()
    return render(request, 'Auto_DjangoWeb_IvanovLev/add_catalog_item.html', {'form': form})

def is_manager(user):
    return user.is_staff

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = CatalogItem.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    return render(request, 'Auto_DjangoWeb_IvanovLev/cart.html', {'items': items, 'total': total})


@login_required
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    order = Order.objects.create(user=request.user, total_price=0)
    total = 0
    for product_id, quantity in cart.items():
        product = CatalogItem.objects.get(id=product_id)
        OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
        total += product.price * quantity
    order.total_price = total
    order.save()

    request.session['cart'] = {}
    return redirect('my_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'Auto_DjangoWeb_IvanovLev/my_orders.html', {'orders': orders})


@user_passes_test(is_manager)
def manager_orders(request):
    orders = Order.objects.all()
    return render(request, 'Auto_DjangoWeb_IvanovLev/manager_orders.html', {'orders': orders})


@user_passes_test(is_manager)
def order_status(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.status = request.POST.get('status')
        order.save()
    return redirect('manager_orders')