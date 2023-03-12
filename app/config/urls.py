"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include

from tealist import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("vendors/list", views.VendorListView, name="vendors"),
    path("vendors/<str:slug>/", views.VendorDetailView, name="vendor-detail"),
    path("vendors/<str:slug>/comments/", views.CommentsView, name="comments"),
    path("releases/", views.ReleaseHistory, name="releases"),
    path("accounts/", include("allauth.urls")),                                     # Used by django-allauth
    path('__debug__/', include('debug_toolbar.urls')),                              # Used by Django debug doolbat
]
