import requests
from urllib.request import urlopen
import urllib.parse
import json
from datetime import datetime
from tealist.models import Vendor, Tea, TeaVariant, Variety
from djmoney.money import Money
import re
from thefuzz import fuzz

test_vendors = ["https://essenceoftea.com/", "https://kingteamall.com"]


def run():
    vendors = Vendor.objects.all()
    varities = Variety.objects.all()

    for vendor in vendors:
        # Checks if the site has an accessible products.json, and loads it if so

        try:
            response = requests.request(
                "GET", f"{vendor.url.removesuffix('/')}/products.json?limit=250"
            )
            products = json.loads(response.text)
            products = products["products"]
        except:
            continue

        print(vendor.url)

        Tea.objects.filter(vendor=vendor).all().delete()

        # Fetches the store's currency from a common Shopify <script>

        try:
            response = requests.request("GET", vendor.url)
            finder = re.search(r"Shopify\.currency = (.*?;)", response.text).group(1)
            finder = json.loads(finder.removesuffix(";"))
            currency = finder["active"]
        except:
            currency = "NON"

        # Creates the Tea and TeaVariant models

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

            def CheckAgainstAliases(text):
                for variety in varities:
                    for a in variety.alias:
                        if fuzz.ratio(text, a) > 70:
                            tea.variety.add(variety)

            title_list = product["title"].split()
            for word in title_list:
                CheckAgainstAliases(word)

            for tag in product["tags"]:
                for word in tag.split():
                    CheckAgainstAliases(word)

            if product["variants"]:
                for variant in product["variants"]:
                    teaVariant = TeaVariant.objects.create(
                        tea=tea,
                        title=variant["title"],
                        price=Money(variant["price"], currency),
                    )

                if variant["compare_at_price"] and float(variant["compare_at_price"]) < 1:
                    teaVariant.compare_at_price = Money(
                        variant["compare_at_price"], currency
                    )
                    tea.on_sale = True
                else:
                    continue

                teaVariant.save()

            tea.save()
