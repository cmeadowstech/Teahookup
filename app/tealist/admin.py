from django.contrib import admin
from tealist.models import *
import csv
from django.http import HttpResponse

admin.site.register(Location)
admin.site.register(Variety)
admin.site.register(Rating)
admin.site.register(Tea)
admin.site.register(TeaVariant)


class UpdateVendor:
    def enable_featured(self, request, queryset):
        for Vendor in queryset:
            Vendor.featured = True
            Vendor.save()

    def disable_featured(self, request, queryset):
        for Vendor in queryset:
            Vendor.featured = False
            Vendor.save()

    def enable_active(self, request, queryset):
        for Vendor in queryset:
            Vendor.active = True
            Vendor.save()

    def disable_active(self, request, queryset):
        for Vendor in queryset:
            Vendor.active = False
            Vendor.save()

    enable_featured.short_description = "Enable Featured"
    disable_featured.short_description = "Disabled Featured"
    enable_active.short_description = "Activate vendor"
    disable_active.short_description = "Deactivate vendor"


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin, ExportCsvMixin, UpdateVendor):
    list_display = ("name", "url", "created", "featured", "rating", "active")
    list_filter = ("store_location", "ship_to", "tea_source")

    filter_horizontal = ("variety",)

    fieldsets = (
        (None, {"fields": ("name", "description", "variety")}),
        ("URLs", {"fields": [("url", "url_alt")]}),
        (
            "Locations",
            {
                "classes": ("extrapretty",),
                "fields": [("store_location", "ship_to", "tea_source")],
            },
        ),
        (
            "Advanced",
            {
                "classes": ("collapse",),
                "fields": [("featured", "established"), "slug", "rating", "active"],
            },
        ),
    )

    actions = [
        "export_as_csv",
        "enable_featured",
        "disable_featured",
        "enable_active",
        "disable_active",
    ]


@admin.register(comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("created_on", "vendor", "user", "value", "active")
    search_fields = ["user__username", "vendor__name"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


admin.site.register(Profile)
