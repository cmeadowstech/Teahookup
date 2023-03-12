from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .filters import *
from .forms import CommentForm

# Helper logic


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
    f = VendorFilter(request.GET, queryset=vendor.objects.all())
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
    Recent = vendor.objects.all().order_by('created')[:5]

    context = {"Featured" : Featured, "Recent": Recent}

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
                Comment = comment.objects.create(
                    vendor=Vendor, user=request.user, content=content
                )
                Comment.save()

                response = "Thanks for sharing your thoughts! Refresh to see your comment."
                return HttpResponse(response)
    else:
        cf = CommentForm()

    context = {"vendor": Vendor, "comments": Comments, "comment_form": cf}

    return render(request, "comments_partial.html", context)
