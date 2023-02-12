from django.contrib import admin
from tealist.models import vendor, location, variety

# Register your models here.

admin.site.register(vendor)
admin.site.register(location)
admin.site.register(variety)