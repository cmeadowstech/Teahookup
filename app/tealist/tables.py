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
        html = f'''
        <a href="{ record.get_absolute_url() }" hx-get="{ record.get_absolute_url() }" hx-target="#htmx_modal" hx-trigger="click"
            hx-on:click="daisy_modal.showModal()" class="font-serif font-bold border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out text-left">
            {value}
        </a>
        '''
        return format_html(html)
    
    def render_url(self, value):
        return format_html(f'<a href="{value}" class="text-secondary border-b border-transparent hover:border-b hover:border-secondary transition ease-in-out" target="_blank">{value}</a>')
    
    def render_description(self, value):
        return value
    
    def render_store_location(self, value):
        locations = list(value.all().values_list('name', flat=True))
                
        return format_html(f'<span class="text-accent">{", ".join(locations)}</span>')
    
    def render_tea_source(self, value):
        locations = list(value.all().values_list('name', flat=True))
                
        return format_html(f'<span class="text-accent">{", ".join(locations)}</span>')
    
    def render_variety(self, value):
        varieties = list(value.all().values_list('name', flat=True))
                
        return format_html(f'<span class="text-accent">{", ".join(varieties)}</span>')