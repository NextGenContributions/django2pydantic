"""Models for testing ManyToMany fields. Test for them can't work without migrations."""
# pyright: reportUnannotatedClassAttribute=false
# ruff: noqa: DJ008

from django.db import models


class ForeignModel(models.Model):
    """Foreign model for testing."""

    id = models.AutoField(primary_key=True)


class M2MOptional(models.Model):
    """Foreign model for testing."""

    id = models.AutoField(primary_key=True)
    field = models.ManyToManyField(ForeignModel, blank=True)


class M2MRequired(models.Model):
    """Foreign model for testing."""

    id = models.AutoField(primary_key=True)
    field = models.ManyToManyField(ForeignModel, blank=False)
