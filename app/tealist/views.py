from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import requests, json
import environ

from .models import *
from .filters import *
from .forms import *

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
    f = VendorFilter(request.GET, queryset=vendor.objects.prefetch_related('tea_source','ship_to','variety','store_location').all().exclude(active=False).order_by('created','id'))

    response = GetPages(f.qs, 6, request)
    parameters = GetParams(request)

    context = {
        "filter": response,
        "filter_form": f,
        "parameters": parameters,
    }

    return context


def GetCollectionsContext(request):
    f = CollectionFilter(request.GET, queryset=collection.objects.prefetch_related('rating').select_related('user').all())

    response = GetPages(f.qs, 6, request)
    parameters = GetParams(request)

    context = {
        "filter": response,
        "filter_form": f,
        "parameters": parameters,
    }

    topCollections = (
        collection.objects.prefetch_related('rating').select_related('user').all()
        .annotate(num_rating=Count("rating"))
        .order_by("-num_rating")[:5]
    )
    if request.user.is_authenticated:
        userCollections = collection.objects.select_related('user').filter(user=request.user).order_by(
            "-created_on"
        )[:5]
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


def index(request):
    Featured = vendor.objects.filter(featured=True)
    Recent = vendor.objects.all().order_by("created")[:3]

    context = {"Featured": Featured, "Recent": Recent}

    return render(request, "index.html", context)


def VendorListView(request):
    context = GetVendorsContext(request)

    if request.htmx:
        template = "vendor_list_partial.html"
    else:
        template = "vendor_list.html"

    return render(
        request,
        template,
        context,
    )


def VendorDetailView(request, slug):
    Vendor = get_object_or_404(vendor, slug=slug)
    context = {}
    context["vendor"] = Vendor

    context["related_collections"] = collection.objects.filter(vendors__id=Vendor.id)[
        :5
    ]

    context["regional_vendors"] = vendor.objects.filter(
        tea_source__id__in=Vendor.tea_source.all()
    ).exclude(id=Vendor.id)[:5]
    context["comment_form"] = CommentForm()

    if request.htmx:
        template = "vendor_detail_partial.html"
    else:
        template = "vendor_detail.html"

    return render(request, template, context)


def CommentsView(request, slug):
    Vendor = get_object_or_404(vendor, slug=slug)
    Comments = Vendor.comments.filter(active=True)

    if request.method == "POST":
        if Comments.filter(user=request.user):
            response = "Please only one comment per user. If you want to add additional information, you can edit your previous comment."
            return HttpResponse(response)
        else:
            cf = CommentForm(request.POST or None)
            if cf.is_valid():
                content = request.POST.get("content")
                value = request.POST.get("value")
                Comment = comment.objects.create(
                    vendor=Vendor, user=request.user, content=content, value=value
                )
                Comment.save()

                response = (
                    "Thanks for sharing your thoughts! Refresh to see your comment."
                )
                return HttpResponse(response)
    else:
        cf = CommentForm()

    context = {"vendor": Vendor, "comments": Comments, "comment_form": cf}

    return render(request, "comments_partial.html", context)


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

@login_required
def ProfileView(request):
    userCollections = collection.objects.filter(user=request.user).order_by(
        "-created_on"
    )

    context = {"userCollections": userCollections}

    return render(request, "profile.html", context)


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

    return render(request, "vendor_submit.html", context)


def CollectionNewView(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)

        if form.is_valid():
            Collection = form.save(commit=False)
            Collection.user = request.user
            Collection.save()
            Collection.vendors.set(
                vendor.objects.filter(id__in=dict(request.POST)["vendors"])
            )

            messages.success(request, f"Thanks for submitting { Collection.name }!")

            context = {"form": form}
        else:
            context = {"form": form}

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CollectionForm()

    form = CollectionForm()
    context = {"form": form}

    return render(request, "collections/collections_new.html", context)


def CollectionListView(request):
    context = GetCollectionsContext(request)

    if request.htmx:
        template = "collections/collections_list_partial.html"
    else:
        template = "collections/collections_list.html"

    return render(request, template, context)


def CollectionPreviewView(request):
    Vendors = vendor.objects.filter(id__in=dict(request.POST)["vendors"])
    Name = request.POST["name"]
    Content = request.POST["content"]
    context = {"vendors": Vendors, "name": Name, "content": Content}

    return render(request, "collections/collections_new_preview.html", context)


def CollectionDetailView(request, slug):
    context = {}
    Collection = get_object_or_404(collection.objects.select_related('user'), slug=slug)
    context["collection"] = Collection

    return render(request, "collections/collection_detail.html", context)


def CollectionRating(request, slug):
    Collection = collection.objects.get(slug=slug)

    if request.user in Collection.rating.all():
        Collection.rating.remove(request.user)
    else:
        Collection.rating.add(request.user)

    return HttpResponse(f"+{Collection.rating.all().count()}")
