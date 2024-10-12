# %% [markdown]
# Lets define some example Django models with all the relationships we can think of:

# %%
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

# Setup Django
django.setup()

from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    class Meta:
        app_label = "tests"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(help_text="Publisher's official address")

    class Meta:
        app_label = "tests"


class BookAuthor(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_added = models.DateField()

    class Meta:
        app_label = "tests"
        default_related_name = "book_authors"
        unique_together = ("book", "author")


class BookDetails(models.Model):
    description = models.TextField()

    class Meta:
        app_label = "tests"
        default_related_name = "book_details"


class Book(models.Model):
    """Book model example with all the relationships we can think of."""

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField(null=True)
    book_details = models.OneToOneField(
        BookDetails,
        on_delete=models.CASCADE,
        null=True,
    )
    authors = models.ManyToManyField(
        Author,
        through=BookAuthor,
    )  # Many-to-Many relationship
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
    )  # Foreign Key relationship

    class Meta:
        app_label = "tests"
        default_related_name = "books"


class Library(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    class Meta:
        app_label = "tests"


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Foreign Key relationship
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
    )  # Foreign Key relationship
    inventory_number = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = "tests"
        default_related_name = "book_copies"


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign Key relationship
    book_copy = models.ForeignKey(
        BookCopy,
        on_delete=models.CASCADE,
    )  # Foreign Key relationship
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "tests"
        default_related_name = "borrowings"


# %% [markdown]
# Now lets do some testing:

# %%
from typing import ClassVar

from rich import print_json

from superschema.schema import SuperSchema
from superschema.types import Infer, ModelFields


class BookSchema(SuperSchema):
    """Book schema example with nested fields."""

    class Meta(SuperSchema.Meta):
        """Here we define the model and the fields we want to infer."""

        model = Book
        fields: ClassVar[ModelFields] = {
            "title": Infer,
            "isbn": Infer,
            "publication_date": Infer,
            "book_details": {"description": Infer},
            "authors": {"name": Infer},
            "publisher": {"name": Infer},
            "book_copies": {"library": Infer},  # note: here we use a reverse relation
        }


print_json(data=BookSchema.model_json_schema())
