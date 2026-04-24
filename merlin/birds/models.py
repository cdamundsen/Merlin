from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class Order(models.Model):
    """
    Keeps track of the all the Orders
    """
    name = models.CharField(
        max_length=128,
        unique=True
    )
    slug = models.SlugField(
        max_length=128
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    wikipedia_link = models.URLField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse(
            'birds:order-detail',
            args=[self.slug]
        )

    def save(self, *args, **kwargs):
        """
        Override the save method so the slug gets created
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Family(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True
    )
    slug = models.SlugField(
        max_length=128
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='families'
    )
    wikipedia_link = models.URLField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse(
            'birds:family-detail',
            args=[
                self.slug
            ]
        )

    def save(self, *args, **kwargs):
        """
        Override the save method so the slug gets created
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genus(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(
        max_length=128
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='genuses'
    )
    wikipedia_link = models.URLField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse(
            'birds:genus-detail',
            args=[
                self.slug,
            ]
        )

    def save(self, *args, **kwargs):
        """
        Override the save method so the slug gets created
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Species(models.Model):
    """
    Keeps track of each Species. At this time the name must be unique.
    The species does not have that restriction since in genus species pairs
    it is possible for the species to be seen more than once. For example
    Haemorhous mexicanus and quiscalus mexicanus
    """
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=256
    )
    species = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    genus = models.ForeignKey(
        Genus,
        on_delete=models.CASCADE,
        related_name='species',
        null=True,
        blank=True
    )
    cornell_link = models.URLField(
        null=True,
        blank=True
    )
    wikipedia_link = models.URLField(
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse(
            'birds:species-detail',
            args=[
                self.slug
            ]
        )

    class Meta:
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return  super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=256
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    wikipedia_link = models.URLField(
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse(
            'birds:location-detail',
            args=[
                self.slug
            ]
        )

    class Meta:
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    date = models.DateField()
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='events'
    )
    slug = models.SlugField(
        max_length=266
    )
    duration = models.DurationField(
        blank=True,
        null=True
    )
    birds = models.ManyToManyField(
        Species,
        related_name='events'
    )
    comment = models.TextField(
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse(
            'birds:event-detail',
            args=[
                self.slug
            ]
        )

    class Meta:
        ordering = ['-date',]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['location']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.location.name} {self.date}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} on {self.date} {self.birds.count()} birds detected"