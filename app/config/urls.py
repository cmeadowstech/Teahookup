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
from django.conf import settings
from django.conf.urls.static import static

from tealist import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("vendors/list", views.VendorListView, name="vendors"),
    path("vendors/table", views.VendorTableView.as_view(), name="vendors-table"),
    path("vendors/submit/", views.VendorSubmitView, name="vendors_submit"),
    path("vendors/<str:slug>/", views.VendorDetailView, name="vendor-detail"),
    path("vendors/<str:slug>/rate", views.VendorRating, name="vendor-rate"),
    path("collections/list/", views.CollectionListView, name="collections"),
    path("collections/new/", views.CollectionNewView, name="collections_new"),
    path(
        "collections/new/preview/",
        views.CollectionPreviewView,
        name="collections_new_preview",
    ),
    path(
        "collections/<str:slug>/", views.CollectionDetailView, name="collection-detail"
    ),
    path("collections/<str:slug>/rate", views.CollectionRating, name="collection-rate"),
    path("releases/", views.ReleaseHistory, name="releases"),
    path("privacy/", views.PrivacyPolicy, name="privacy"),
    path("terms/", views.TermsAndConditions, name="terms"),
    path("error/", views.returnError, name="error"),
    path("helloWorld/", views.helloWorld, name="helloWorld"),
    path("accounts/", include("allauth.urls")),  # Used by django-allauth
    path(
        r"comments/", include("django_comments_xtd.urls")
    ),  # Used by django-comments-xtd
    path("accounts/profile/", views.ProfileView, name="profile"),
    path("accounts/profile/update", views.ProfileUpdate, name="profile_update"),
    path("__debug__/", include("debug_toolbar.urls")),  # Used by Django debug toolbar
    path(
        "__reload__/", include("django_browser_reload.urls")
    ),  # Used by django-tailwind[reload]
    path(
        "cookie_consent_check/", views.CookieConsentCheck, name="cookie_consent_check"
    ),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
