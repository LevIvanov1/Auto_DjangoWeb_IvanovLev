"""
Auto_DjangoWeb_IvanovLev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from auto import forms, views
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from datetime import datetime
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('links/', views.links, name='links'),
    path('contacts/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('pool/', views.pool, name='pool'),
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(
            template_name='Auto_DjangoWeb_IvanovLev/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context={
                'title': 'Вход',
                'year': datetime.now().year,
            },
        ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),

    # -
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]


# https://apps.openedu.ru/learning/course/course-v1:spbstu+WEBPYT+spring_2026/block-v1:spbstu+WEBPYT+spring_2026+type@sequential+block@7aede4c4d9ec40879036bd20ca092fc3/block-v1:spbstu+WEBPYT+spring_2026+type@vertical+block@708c1f3a749545b381158cc4d861fea3