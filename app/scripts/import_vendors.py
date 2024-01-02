from tealist.models import Vendor, Location, Variety
import csv


def run():
    with open("test_vendor_list.csv") as file:
        reader = csv.reader(file)
        next(reader)

        Vendor.objects.all().delete()

        for row in reader:
            new_vendor = Vendor(
                url=row[0],
                url_alt=row[1],
                name=row[2],
                featured=False,
                description=row[7],
                active=True,
            )

            new_vendor.save()

            store_locations = row[3].split(",")
            for l in store_locations:
                store_location, _ = Location.objects.get_or_create(name=l.strip())
                new_vendor.store_location.add(store_location)

            ships_to = row[4].split(",")
            for to in ships_to:
                ship_to, _ = Location.objects.get_or_create(name=to.strip())
                new_vendor.ship_to.add(ship_to)

            tea_sources = row[5].split(",")
            for source in tea_sources:
                tea_source, _ = Location.objects.get_or_create(name=source.strip())
                new_vendor.tea_source.add(tea_source)

            Varieties = row[6].split(",")
            for v in Varieties:
                Variety, _ = Variety.objects.get_or_create(name=v.strip())
                new_vendor.Variety.add(Variety)
