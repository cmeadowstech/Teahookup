from django.db import models
from djmoney.models.fields import MoneyField
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid, json
from django.db.models import Count
from meta.models import ModelMeta

def GenerateGuid():
    return str(uuid.uuid4())[:4]

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Delete profile when user is deleted
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"  # show how we want it to be displayed


class Location(models.Model):
    name = models.CharField(max_length=30, help_text="Country/region name", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Locations"


class Variety(models.Model):
    name = models.CharField(
        max_length=30, help_text="Type of tea or offering", unique=True
    )
    alias = ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
            blank=True,
            default=list
        )
    description = models.TextField(
        help_text="Description of this type of tea", blank=True
    )

    def __str__(self):
        return self.name


class Vendor(ModelMeta, models.Model):
    name = models.CharField(
        max_length=30, help_text="Business name of the vendor", unique=True
    )
    url = models.URLField(help_text="URL for this vendor's store", unique=True)
    url_alt = models.URLField(
        help_text="Alternate URL for this vendor's store.", blank=True
    )
    description = models.TextField(help_text="Description of the vendor", blank=True)
    store_location = models.ManyToManyField(
        Location,
        help_text="Select locations this vendor ships from",
        blank=True,
        related_name="store_location",
    )
    ship_to = models.ManyToManyField(
        Location,
        help_text="Select locations this vendor ships to",
        blank=True,
        related_name="ship_to",
    )
    tea_source = models.ManyToManyField(
        Location,
        help_text="Select locations this vendor sources tea from",
        blank=True,
        related_name="tea_source",
    )
    featured = models.BooleanField(default=False)
    variety = models.ManyToManyField(
        Variety, help_text="Select the varieties of tea this vendor sells", blank=True
    )
    established = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=0.0)
    active = models.BooleanField(default=False)

    _metadata = {
        'title': 'meta_title',
        'description': "Looking for a new tea vendor? Search our list of vendors to find the perfect tea offerings for your next cup."
    }
    
    def meta_title(self):
        if self.name:
            return f'Tea Hookup | {self.name}'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/vendors/%s/" % self.slug

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class comment(models.Model):
    RATING_CHOICES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    value = models.IntegerField(choices=RATING_CHOICES)

    def save(self, *args, **kwargs):
        v = self.vendor
        Comments = comment.objects.filter(vendor=v)
        avg = float(0)
        for c in Comments:
            avg += float(c.value)

        avg += float(self.value)
        avg = avg / (len(Comments) + 1)
        Vendor.rating = avg
        Vendor.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_on"]
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "user"], name="One comment per user per vendor"
            )
        ]


class Collection(models.Model):
    unique_id = models.CharField(
        max_length=6, default=GenerateGuid(), editable=False
    )
    name = models.CharField(
        max_length=40, help_text="What do you want to call this vendor"
    )
    vendors = models.ManyToManyField(
        Vendor,
        help_text="Which vendors belong to this collection",
        related_name="collection_vendors",
    )
    private = models.BooleanField(default=True)
    content = models.TextField(help_text="Info about this collection", blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collection_owner"
    )
    active = models.BooleanField(default=True)
    rating = models.ManyToManyField(User, related_name="collection_voters", blank=True)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/collections/%s/" % self.slug

    def get_location_stats(self):
        location_count = (
            Location.objects.prefetch_related("Vendor")
            .filter(tea_source__in=self.vendors.all())
            .annotate(location_count=Count("tea_source"))
        )

        return json.dumps(list(location_count.values("name", "location_count")))

    def save(self, *args, **kwargs):
        value = f"{self.name}-{self.unique_id}"
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Rating(models.Model):
    RATING_CHOICES = (
        (5, "5"),
        (4.5, "4.5"),
        (4, "4"),
        (3.5, "3.5"),
        (3, "3"),
        (2.5, "2.5"),
        (2, "2"),
        (1.5, "1.5"),
        (1, "1"),
        (0.5, "0.5"),
    )

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vendor_rating"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, choices=RATING_CHOICES
    )

    class Meta:
        verbose_name_plural = "Ratings"
        unique_together = ("vendor", "user")

    def __str__(self):
        return f"{self.vendor} - {self.user} | {self.value}"


class Tea(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    published_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True)
    handle = models.CharField(max_length=256)
    variety = models.ManyToManyField(
        Variety, blank=True, default=""
    )
    on_sale = models.BooleanField(default=False)

    class Meta:
        unique_together = ("vendor", "handle")

    def __str__(self):
        return f"{self.vendor} | {self.title}"


class TeaVariant(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE, related_name="tea_variant", verbose_name="Price")
    title = models.CharField(max_length=256)
    price = MoneyField(max_digits=14, decimal_places=2, null=True, default_currency=None)
    compare_at_price = MoneyField(max_digits=14, decimal_places=2, null=True, default_currency=None)

    class Meta:
        unique_together = ("tea", "title")

    def __str__(self):
        return f"{self.tea} | {self.title}"
