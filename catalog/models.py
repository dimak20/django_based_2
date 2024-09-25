from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from library import settings


class LiteraryFormat(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=63, null=True, blank=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    format = models.ForeignKey(LiteraryFormat, on_delete=models.CASCADE, related_name="books")
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to="labels", null=True, blank=True)
    boolean = models.BooleanField(default=False)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} (price: {self.price}), format: {self.format.name}"

    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])
