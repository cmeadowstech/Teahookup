import django_tables2 as tables
from django.utils.html import format_html


from .models import *


class VendorTable(tables.Table):
    class Meta:
        model = Vendor
        fields = (
            "name",
            "url",
            "description",
            "store_location",
            "tea_source",
            "variety",
        )
        order_by = "-created"

    def render_name(self, value, record):
        html = f"""
        <a href="{ record.get_absolute_url() }" hx-get="{ record.get_absolute_url() }" hx-target="#htmx_modal" hx-trigger="click"
            hx-on:click="daisy_modal.showModal()" class="font-serif font-bold border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out text-left">
            {value}
        </a>
        """
        return format_html(html)

    def render_url(self, value):
        return format_html(
            f'<a href="{value}" class="text-secondary border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out" target="_blank">{value}</a>'
        )

    def render_description(self, value):
        return value

    def render_store_location(self, value):
        locations = list(value.all().values_list("name", flat=True))

        return format_html(f'<span class="text-accent">{", ".join(locations)}</span>')

    def render_tea_source(self, value):
        locations = list(value.all().values_list("name", flat=True))

        return format_html(f'<span class="text-accent">{", ".join(locations)}</span>')

    def render_variety(self, value):
        varieties = list(value.all().values_list("name", flat=True))

        return format_html(f'<span class="text-accent">{", ".join(varieties)}</span>')


class TeaTable(tables.Table):
    tea_variant = tables.Column(verbose_name="Price")

    class Meta:
        model = Tea
        fields = ("title", "vendor", "tea_variant", "variety")
        order_by = "-created_at"

    def render_title(self, value, record):
        html = f"""
        <span class="flex justify-between w-full">
            <p>{value}</p>
            <a href="{record.vendor.url.removesuffix('/')}/products/{ record.handle }" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                </svg>
            </a>
        </span>
        """

        return format_html(html)

    def render_vendor(self, value):
        html = f"""
        <a href="{ value.get_absolute_url() }" hx-get="{ value.get_absolute_url() }" hx-target="#htmx_modal" hx-trigger="click"
            hx-on:click="daisy_modal.showModal()" class="font-serif font-bold border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out text-left">
            {value}
        </a>
        """
        return format_html(html)

    def render_tea_variant(self, value):
        variants = value.all()
        variants_html = []
        for v in variants:
            if v.title == "Default Title":
                variants_html += f"<option>{v.price}</option>"
            else:
                variants_html += f"<option>{v.title} - {v.price}</option>"

        return format_html(
            f'<select class="select w-full max-w-64 min-w-32">{"".join(variants_html)}</select>'
        )

    def render_variety(self, value):
        varieties = list(value.all().values_list("name", flat=True))

        return format_html(f'<span class="text-accent">{", ".join(varieties)}</span>')
