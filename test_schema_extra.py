#!/usr/bin/env python3
"""Test script to explore how to add custom schema extensions in Pydantic."""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
import django
django.setup()

from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field
from pydantic._internal._generate_schema import GetJsonSchemaFunction
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
import json

# Create a test enum with custom schema modifier
class TestEnum(str, Enum):
    A = "a"
    B = "b" 
    C = "c"
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaFunction
    ) -> JsonSchemaValue:
        """Add custom x-enumDescriptions to the enum schema."""
        json_schema = handler(core_schema)
        json_schema['x-enumDescriptions'] = ["Choice A", "Choice B", "Choice C"]
        return json_schema

# Test how to add custom schema properties
class TestModel(BaseModel):
    enum_field: TestEnum

schema = TestModel.model_json_schema()
print("Test schema with custom __get_pydantic_json_schema__:")
print(json.dumps(schema, indent=2))