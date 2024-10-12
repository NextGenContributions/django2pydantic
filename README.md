# Why this package?

# Tags

django,api,rest,json,ninja,infer,django orm, django model, pydantic, schema

# Key feature

# Usage

```python

from django.db import models

class MyModelA(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()


class MyModelB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(MyModelA, on_delete=models.CASCADE)
    applications = models.ManyToManyField(MyModelA)
    account = models.OneToOneField(MyModelA, on_delete=models.CASCADE)

```

```python


#

# Usage example:

from superschema.types import Infer, InferExcept, ModelFields

# Basic usage:

model: ModelFields = {
    "id": Infer,
    "name": Infer,
    "description": Infer,
    "organization": {
        "id": Infer,
        "name": Infer
    },
    "applications": {
        "id": Infer,
        "name": Infer
    },
    "account": {
        "id": Infer,
        "name": Infer
    },
}

# Overriding some inferred details

from superschema.types import InferExcept

list_fields: ModelFields = {
    "name": InferExcept(description="I was not happy what was inferred so I defined here."),
}

# Allows also to use the native Pydantic FieldInfo

from pydantic import Field

list_fields: ModelFields = {
    "description": Field(title="some name"), # pass native Pydantic field details
}

# Using already defined schemas in relations

list_fields: ModelFields = {
    "id": Infer,
    "name": Infer,
    "description": Infer,
    "organization": {
        "id": Infer,
        "name": Infer
    },
    "applications": {
        "id": Infer,
        "name": Infer
    },
    "account": {
        "id": Infer,
        "name": Infer
    },
}


```