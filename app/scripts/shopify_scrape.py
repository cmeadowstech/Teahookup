import requests
import json
from datetime import datetime
from tealist.models import Vendor, Tea, TeaVariant

test_vendors = ["https://essenceoftea.com/", "https://kingteamall.com"]


def run():
    vendors = Vendor.objects.all()

    for vendor in vendors:
        try:
            response = requests.request(
                "GET", f"{vendor.url.removesuffix('/')}/products.json"
            )
            products = json.loads(response.text)
            products = products["products"]
        except:
            continue

        for product in products:
            try:
                tea, created = Tea.objects.update_or_create(
                    vendor=vendor,  # Change this when using QS
                    handle=product["handle"],
                    defaults={
                        "title": product["title"],
                        "published_at": datetime.fromisoformat(product["published_at"]),
                        "created_at": datetime.fromisoformat(product["created_at"]),
                        "updated_at": datetime.fromisoformat(product["updated_at"]),
                    },
                )
            except:
                pass

            if product["variants"]:
                for variant in product["variants"]:
                    variant, created = TeaVariant.objects.update_or_create(
                        tea=tea,
                        title=variant["title"],
                        defaults={
                            "price": variant["price"],
                            "compare_at_price": variant["compare_at_price"],
                        },
                    )
