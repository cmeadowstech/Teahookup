from tealist.models import *
from django.contrib.auth.models import User
import random

Locations = location.objects.all()
Varieties = variety.objects.all()


def GenerateName():
    Name = (
        Locations[random.randint(0, len(Locations) - 1)].name
        + " "
        + Varieties[random.randint(0, len(Varieties) - 1)].name
    )

    return Name


def run():
    Vendors = vendor.objects.all()
    for i in range(11):
        C = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. A erat nam at lectus urna duis convallis. Tincidunt lobortis feugiat vivamus at augue eget. Quam lacus suspendisse faucibus interdum posuere lorem. Quis risus sed vulputate odio. Sit amet cursus sit amet dictum sit. Dictum fusce ut placerat orci. Tortor at auctor urna nunc id. Erat pellentesque adipiscing commodo elit at imperdiet dui accumsan. Velit egestas dui id ornare arcu odio ut sem. Netus et malesuada fames ac turpis egestas sed. Nullam vehicula ipsum a arcu cursus vitae congue mauris. Eros in cursus turpis massa tincidunt dui. A diam maecenas sed enim ut sem viverra aliquet. Consequat ac felis donec et odio pellentesque. Vitae congue eu consequat ac felis donec et. Felis imperdiet proin fermentum leo vel orci porta. Lorem ipsum dolor sit amet consectetur adipiscing elit. Ut venenatis tellus in metus vulputate eu scelerisque felis imperdiet.

Quisque non tellus orci ac auctor augue. Commodo nulla facilisi nullam vehicula ipsum a arcu cursus. Vitae purus faucibus ornare suspendisse sed nisi lacus sed. Vitae elementum curabitur vitae nunc sed velit dignissim. Commodo nulla facilisi nullam vehicula ipsum a arcu cursus. Viverra nam libero justo laoreet sit amet. Et sollicitudin ac orci phasellus egestas tellus. Tempor id eu nisl nunc. Velit scelerisque in dictum non consectetur a erat. Ultrices in iaculis nunc sed augue. Magna ac placerat vestibulum lectus mauris ultrices. Nunc eget lorem dolor sed viverra ipsum nunc aliquet. Turpis egestas pretium aenean pharetra. Aliquet lectus proin nibh nisl condimentum id. Laoreet sit amet cursus sit amet dictum sit.

Sed risus ultricies tristique nulla aliquet enim tortor at auctor. Fringilla phasellus faucibus scelerisque eleifend donec. Luctus accumsan tortor posuere ac ut consequat semper viverra. Ac odio tempor orci dapibus ultrices in iaculis nunc sed. Id semper risus in hendrerit. Morbi blandit cursus risus at ultrices mi. Etiam sit amet nisl purus in. Et malesuada fames ac turpis egestas. Elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Mattis vulputate enim nulla aliquet."""

        new_collection = collection(
            user=User.objects.get(username="cmeadows"), content=C, name=GenerateName()
        )

        new_collection.save()

        Vendors_dic = []

        for i in range(random.randint(3, 11)):
            Vendors_dic.append(Vendors[random.randint(0, len(Vendors) - 1)].id)

        new_collection.vendors.set(vendor.objects.filter(id__in=Vendors_dic))
