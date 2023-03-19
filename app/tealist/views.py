from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
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
    f = VendorFilter(request.GET, queryset=vendor.objects.all().exclude(active=False))
    locations = location.objects.all()

    response = GetPages(f.qs, 6, request)
    parameters = GetParams(request)

    context = {
        "filter": response,
        "filter_form": f,
        "locations": locations,
        "parameters": parameters,
    }

    return context


# Views


def index(request):
    Featured = vendor.objects.filter(featured=True)
    Recent = vendor.objects.all().order_by("created")[:5]

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
    Comments = Vendor.comments.filter(active=True)
    cf = CommentForm()

    if request.htmx:
        template = "vendor_detail_partial.html"
    else:
        template = "vendor_detail.html"

    context = {"vendor": Vendor, "comments": Comments, "comment_form": cf}

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


def ProfileView(request):
    return render(request, "profile.html")


def VendorSubmitView(request):
    
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            Vendor = form.save()
            messages.success(request, f"Thanks for submitting { Vendor.name }. Once it is approved by an admin, it will be become available on the site.")
            
            context = {"vendor_form": form}
        else:
            context = {"vendor_form": form}

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VendorForm()

    context = {"vendor_form": form}

    return render(request, "vendor_submit.html", context)

def CollectionNewView(request):
    
    form = CollectionForm()
    context = {"form": form}

    return render(request, "collections_new.html", context)