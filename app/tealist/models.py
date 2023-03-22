from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid


class location(models.Model):
    name = models.CharField(max_length=30, help_text="Country/region name", unique=True)

    def __str__(self):
        return self.name


class variety(models.Model):
    name = models.CharField(
        max_length=30, help_text="Type of tea or offering", unique=True
    )
    description = models.TextField(
        help_text="Description of this type of tea", blank=True
    )

    def __str__(self):
        return self.name


class vendor(models.Model):
    name = models.CharField(
        max_length=30, help_text="Business name of the vendor", unique=True
    )
    url = models.URLField(help_text="URL for this vendor's store", unique=True)
    url_alt = models.URLField(
        help_text="Alternate URL for this vendor's store.", blank=True
    )
    description = models.TextField(help_text="Description of the vendor", blank=True)
    store_location = models.ManyToManyField(
        location,
        help_text="Select locations this vendor ships from",
        blank=True,
        related_name="store_location",
    )
    ship_to = models.ManyToManyField(
        location,
        help_text="Select locations this vendor ships to",
        blank=True,
        related_name="ship_to",
    )
    tea_source = models.ManyToManyField(
        location,
        help_text="Select locations this vendor sources tea from",
        blank=True,
        related_name="tea_source",
    )
    featured = models.BooleanField(default=False)
    variety = models.ManyToManyField(
        variety, help_text="Select the varieties of tea this vendor sells", blank=True
    )
    established = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, default=0.0)
    active = models.BooleanField(default=False)

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
        vendor, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    value = models.IntegerField(choices=RATING_CHOICES)

    def save(self, *args, **kwargs):
        Vendor = self.vendor
        Comments = comment.objects.filter(vendor=Vendor)
        avg = float(0)
        for c in Comments:
            avg += float(c.value)

        avg += self.value
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


class collection(models.Model):
    unique_id = models.CharField(
        max_length=6, default=str(uuid.uuid4())[:4], editable=False
    )
    name = models.CharField(
        max_length=40, help_text="What do you want to call this vendor"
    )
    vendors = models.ManyToManyField(
        vendor,
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
    slug = models.SlugField(max_length=250, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/collections/%s/" % self.slug

    def save(self, *args, **kwargs):
        value = f"{self.name}-{self.unique_id}"
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
