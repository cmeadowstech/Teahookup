from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .filters import *


# Create your views here.
def index(request):
    return render(request, "index.html")


def VendorListView(request):
    f = VendorFilter(request.GET, queryset=vendor.objects.all())
    paginator = Paginator(f.qs, 4)
    locations = location.objects.all()
    if request.htmx:
        template = "vendor_list_htmx.html"
    else:
        template = "vendor_list.html"

    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    context = {"filter": response, "filter_form": f, "locations": locations}

    return render(
        request,
        template,
        context,
    )
