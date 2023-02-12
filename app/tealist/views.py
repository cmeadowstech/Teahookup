from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .filters import *

# Create your views here.
def index(request):
        return render(request, 'index.html')

def VendorListView(request):
    f = VendorFilter(request.GET, queryset=vendor.objects.all())
    paginator = Paginator(f.qs, 4)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(request, 'vendor_list.html', {'filter': response,'filter_form':f})