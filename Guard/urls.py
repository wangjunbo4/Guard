'''
Author: Gtylcara.
Date: 2021-03-04 20:50:10
LastEditors: Gtylcara.
LastEditTime: 2021-03-12 19:54:03
'''
"""Guard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('battery/', views.battery),
    path('log/', views.log),
    path('login/', views.login),
    path('register/', views.register),
    path('api/login', views.api_login),
    path('api/register', views.api_register),
    path('api/data', views.api_data),
    path('api/control', views.api_control),
]
