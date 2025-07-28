#!/usr/bin/env python3
"""Test script to understand current enum handling and test x-enumDescriptions."""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
import django
django.setup()

from django.db import models
from django.utils.translation import gettext_lazy as _
from tests.utils import get_openapi_schema_from_field

class YearInSchool(models.TextChoices):
    FRESHMAN = "FR", _("Freshman")
    SOPHOMORE = "SO", _("Sophomore")
    JUNIOR = "JR", _("Junior")
    SENIOR = "SR", _("Senior")
    GRADUATE = "GR", _("Graduate")

# Test current behavior
field = models.CharField(max_length=2, choices=YearInSchool.choices)
schema = get_openapi_schema_from_field(field)

print("Current OpenAPI schema:")
import json
print(json.dumps(schema, indent=2))