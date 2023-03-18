from tealist.models import vendor, location, variety
import csv


def run():
    Locations = location.objects.all()
    fields = ["homelat", "homelon", "country", "n"]
    filename = "location_counts.csv"

    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)

        for Location in Locations:
            Count = Location.tea_source.all().count()
            if Count > 0:
                row = ["", "", Location.name, Count]
                writer.writerow(row)
