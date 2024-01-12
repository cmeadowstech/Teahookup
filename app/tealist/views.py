from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
import requests, json
import environ

from .models import *
from .filters import *
from .forms import *

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

# Helper logic

env = environ.Env()


def GetPages(qs, pagination, request):
    paginator = Paginator(qs, pagination)
    page = request.GET.get("page")
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    return p


def GetParams(request):
    _request_copy = request.GET.copy()
    parameters = _request_copy.pop("page", True) and _request_copy.urlencode()

    return parameters


def GetVendorsContext(request):
    f = VendorFilter(
        request.GET,
        queryset=Vendor.objects.prefetch_related(
            "tea_source", "ship_to", "variety", "store_location"
        )
        .all()
        .exclude(active=False)
        .order_by("-created", "id"),
    )

    response = GetPages(f.qs, 6, request)
    parameters = GetParams(request)
    rating_form = RatingForm()

    context = {
        "filter": response,
        "filter_form": f,
        "parameters": parameters,
        "rating_form": rating_form,
    }

    return context


def GetCollectionsContext(request):
    f = CollectionFilter(
        request.GET,
        queryset=Collection.objects.prefetch_related("rating")
        .select_related("user")
        .all(),
    )

    response = GetPages(f.qs, 6, request)
    parameters = GetParams(request)

    context = {
        "filter": response,
        "filter_form": f,
        "parameters": parameters,
    }

    topCollections = (
        Collection.objects.prefetch_related("rating")
        .select_related("user")
        .all()
        .annotate(num_rating=Count("rating"))
        .order_by("-num_rating")[:5]
    )
    if request.user.is_authenticated:
        userCollections = (
            Collection.objects.select_related("user")
            .filter(user=request.user)
            .order_by("-created_on")[:5]
        )
    else:
        userCollections = None

    context = {
        "topCollections": topCollections,
        "userCollections": userCollections,
        "filter": response,
        "filter_form": f,
        "parameters": parameters,
    }

    return context


# Views


# @cache_page(CACHE_TTL)
def index(request):
    Featured = Vendor.objects.filter(featured=True)
    Recent = Vendor.objects.all().order_by("-created", "id")[:3]

    context = {"Featured": Featured, "Recent": Recent}

    return render(request, "index.html", context)


def VendorListView(request):
    context = GetVendorsContext(request)

    if request.htmx:
        template = "vendor/vendor_list_partial.html"
    else:
        template = "vendor/vendor_list.html"

    return render(
        request,
        template,
        context,
    )


def VendorDetailView(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)

    context = {}
    context["vendor"] = vendor
    context["related_collections"] = Collection.objects.filter(vendors__id=vendor.id)[
        :5
    ]
    context["regional_vendors"] = Vendor.objects.filter(
        tea_source__id__in=vendor.tea_source.all()
    ).exclude(id=vendor.id)[:5]
    context["rating_form"] = RatingForm()

    if request.htmx:
        template = "vendor/vendor_detail_partial.html"
    else:
        context["teas"] = Tea.objects.filter(vendor=vendor)[:9].prefetch_related("tea_variant")
        template = "vendor/vendor_detail.html"

    return render(request, template, context)


@require_POST
def VendorRating(request, slug):
    vendor = Vendor.objects.get(slug=slug)

    rating, created = Rating.objects.update_or_create(
        vendor=vendor,
        user=request.user,
        defaults={"value": float(request.POST["value"])},
    )

    vendor.rating = Rating.objects.filter(vendor=vendor).aggregate(Avg("value"))[
        "value__avg"
    ]
    vendor.save()

    return HttpResponse(f"{round(vendor.rating, 1)}")


@cache_page(CACHE_TTL)
def ReleaseHistory(request):
    url = "https://api.github.com/repos/cmeadowstech/tea-list/releases"

    payload = {}
    headers = {
        "Authorization": "Bearer " + env("GH_API_TOKEN"),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    Releases = response.json()

    context = {"Releases": Releases}

    return render(request, "release_history.html", context)


def PrivacyPolicy(request):
    return render(request, "privacy_policy.html")


@cache_page(CACHE_TTL)
def TermsAndConditions(request):
    return render(request, "terms_and_conditions.html")


@login_required
def ProfileView(request):
    userCollections = Collection.objects.filter(user=request.user).order_by(
        "-created_on"
    )

    context = {"userCollections": userCollections}

    return render(request, "profile/profile.html", context)


def ProfileUpdate(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"p_form": p_form}

    return render(request, "profile/profile_pic_update.html", context)


def VendorSubmitView(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            Vendor = form.save()
            messages.success(
                request,
                f"Thanks for submitting { Vendor.name }. Once it is approved by an admin, it will be become available on the site.",
            )

            context = {"vendor_form": form}
        else:
            context = {"vendor_form": form}

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VendorForm()

    context = {"vendor_form": form}

    return render(request, "vendor/vendor_submit.html", context)


def CollectionNewView(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)

        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            collection.vendors.set(
                Vendor.objects.filter(id__in=dict(request.POST)["vendors"])
            )

            messages.success(request, f"Thanks for submitting { collection.name }!")

            context = {"form": form}

            return redirect(collection.get_absolute_url())
        else:
            context = {"form": form}

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CollectionForm()

    form = CollectionForm()
    context = {"form": form}

    return render(request, "collection/collections_new.html", context)


def CollectionListView(request):
    context = GetCollectionsContext(request)

    if request.htmx:
        template = "collection/collections_list_partial.html"
    else:
        template = "collection/collections_list.html"

    return render(request, template, context)


def CollectionPreviewView(request):
    Vendors = Vendor.objects.filter(id__in=dict(request.POST)["vendors"])
    Name = request.POST["name"]
    Content = request.POST["content"]
    context = {"vendors": Vendors, "name": Name, "content": Content}

    return render(request, "collection/collections_new_preview.html", context)


def CollectionDetailView(request, slug):
    context = {}
    collection = get_object_or_404(Collection.objects.select_related("user"), slug=slug)
    context["collection"] = collection

    return render(request, "collection/collection_detail.html", context)


def CollectionRating(request, slug):
    collection = Collection.objects.get(slug=slug)

    if request.user in collection.rating.all():
        collection.rating.remove(request.user)
    else:
        collection.rating.add(request.user)

    return HttpResponse(f"+{collection.rating.all().count()}")


def returnError(request):
    division_by_zero = 1 / 0
    return division_by_zero


def helloWorld(request):
    return HttpResponse("Hello world!")


@require_POST
def CookieConsentCheck(request):
    request.session["CookieConsentCheck"] = True

    return HttpResponse(status=200)
