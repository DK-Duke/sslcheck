"""ssll URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from myapp.views import sayhello, djpost, addomain, show, listt, post1, list, delete, grab, grab2, grab3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sayhello),
    path('djpost', djpost),
    path('addomain', addomain),
    path('show/', show),
    path('list/', list),
    path('post1/', post1),
    re_path(r'^delete/(\d+)/$', delete),
    path('grab/', grab),
    re_path(r'^grab2/(\d+)/$', grab2),
    path('grab3', grab3)
]
