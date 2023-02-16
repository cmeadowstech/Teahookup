from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    featured = models.BooleanField()
    variety = models.ManyToManyField(
        variety, help_text="Select the varieties of tea this vendor sells", blank=True
    )
    established = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug}
        return reverse("vendor", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
