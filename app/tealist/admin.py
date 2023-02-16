from django.contrib import admin
from tealist.models import vendor, location, variety
import csv
from django.http import HttpResponse

admin.site.register(location)
admin.site.register(variety)

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(vendor)
class VendorAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'url', 'created')
    list_filter = ('store_location', 'ship_to', 'tea_source')

    filter_horizontal = ('variety',) 

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'variety')
        }),
        ('URLs', {
            'fields': [('url', 'url_alt')]
        }),
        ('Locations', {
            'classes': ('extrapretty',),
            'fields': [('store_location', 'ship_to', 'tea_source')]
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': [('featured', 'established'), 'slug']
        }),
    )

    actions = ["export_as_csv"]



