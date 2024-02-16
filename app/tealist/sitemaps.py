from django.contrib.sitemaps import Sitemap
from .models import Vendor


class VendorSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Vendor.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created
