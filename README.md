![PyPI - License](https://img.shields.io/pypi/l/django)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django2pydantic)

# Why

django2pydantic is the most complete Pydantic schemas based on Django models.

# What

django2pydantic is a library that allows to define Pydantic schemas based on Django database models.

Similar libraries:

- [Djantic](https://jordaneremieff.github.io/djantic/)
- [Django Ninja Schema](https://django-ninja.dev/guides/response/django-pydantic/)
- [Ninja Schema](https://github.com/eadwinCode/ninja-schema)

# Key features

- Supports all Django model field types
- Supports @property decorated Django model methods
- Supports all Django model relation fields:
  - ForeignKey, OneToOneField, ManyToManyField
  - The reverse relations of the above (ManyToOneRel, OneToOneRel, ManyToManyRel)
- Supports defining nested relations
- Provides as complete OpenAPI schema details as possible
- Support for [SchemaField](https://pypi.org/project/django-pydantic-field/)

# How to use

See the following usage examples:

- [Basic usage example](examples/example.ipynb)
- [Overriding Django field properties by using `InferExcept`](examples/overriding-django-field-properties-with-InferExcept.ipynb)
- [Making required Django fields optional in Pydantic schema](examples/making-fields-optional-with-InferExcept.ipynb)

# Some details

## Django fields blank and null

There are some nuances related to the use of `blank` and `null` in Django fields
and how they impact the output pydantic types, but generally:
- If `null=True` the output **type** will be `Optional` (i.e. `str | None`).
- If `blank=True` the field will be **optional** (with **exceptions**).
This is to be more in line with the Django admin/form validation behavior.
- Whether the field is **required** is determined by the **default** value (can be overridden).
  - If the **default** is `PydanticUndefined`, the field is always **required**.
  - If the **default** is `None` (or `""` in case of string), the field is **optional**.
- If `null=False` and `blank=True`, the field typically requires implementing `clean()`
on the model in order to programmatically supply any missing values. In our case, the
**required**/**default** value can vary depending on field type in a way that user
does not need to concern with implementing `clean()`.

### String-based fields
This covers the following Django field types:
- CharField
- SlugField
- EmailField
- URLField
- TextField

| Configuration             | Required     | Default<br>(If not specified) | Type          | Min length | Comments                                                                                                                                                               |
|---------------------------|--------------|-------------------------------|---------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `null=True, blank=True`   | Optional     | `None`                        | `str \| None` | `None`     | There's 2 ways to represent "no data" in the DB: `null` and `""` (**not recommended**)                                                                                 |
| `null=True, blank=False`  | **Required** | `PydanticUndefined`           | `str \| None` | `1`        | • There's 2 ways to represent "no data" in the DB: `null` and `""` (**not recommended**)<br>• However, with **min_length**, we eliminate `""` from being a valid input |
| `null=False, blank=True`  | Optional     | `""`                          | `str`         | `None`     | **Default** is `""` since `null` is not allowed                                                                                                                        |
| `null=False, blank=False` | **Required** | `PydanticUndefined`           | `str`         | `1`        |                                                                                                                                                                        |


### Non-string-based fields
This covers the following Django field types:
- IntegerField
- SmallIntegerField
- IntegerField
- BigIntegerField
- PositiveSmallIntegerField
- PositiveIntegerField
- PositiveBigIntegerField
- FloatField
- DecimalField
- BinaryField
- BooleanField
- DateField
- DateTimeField
- DurationField
- FileField
- FilePathField
- GenericIPAddressField
- ImageField
- JSONField
- TimeField
- UUIDField

**[FieldType]** varies depending on the Django field type

| Configuration             | Required     | Default<br>(If not specified) | Type                  | Comments                                                                                                                                                |
|---------------------------|--------------|-------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `null=True, blank=True`   | Optional     | `None`                        | `[FieldType] \| None` |                                                                                                                                                         |
| `null=True, blank=False`  | **Required** | `PydanticUndefined`           | `[FieldType] \| None` |                                                                                                                                                         |
| `null=False, blank=True`  | **Required** | `PydanticUndefined`           | `[FieldType]`         | Unlike string-based fields, without a specified **default** value, there's no valid empty value to be stored in database thus making this **required**  |
| `null=False, blank=False` | **Required** | `PydanticUndefined`           | `[FieldType]`         |                                                                                                                                                         |


### Relational fields
This covers the following Django field types:
- ForeignKey
- OneToOneField
- ManyToManyField
- ManyToOneRel
- OneToOneRel
- ManyToManyRel

**[PkType]** varies depending on model's primary key type

#### ForeignKey, OneToOneField
| Configuration             | Required     | Default<br>(If not specified) | Type               | Comments                                                                                                                                               |
|---------------------------|--------------|-------------------------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `null=True, blank=True`   | Optional     | `None`                        | `[PkType] \| None` |                                                                                                                                                        |
| `null=True, blank=False`  | **Required** | `PydanticUndefined`           | `[PkType] \| None` |                                                                                                                                                        |
| `null=False, blank=True`  | **Required** | `PydanticUndefined`           | `[PkType]`         | Unlike string-based fields, without a specified **default** value, there's no valid empty value to be stored in database thus making this **required** |
| `null=False, blank=False` | **Required** | `PydanticUndefined`           | `[PkType]`         |                                                                                                                                                        |

#### ManyToManyField
`null` has no effect since there is no way to require a relationship at the database level.
Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#manytomanyfield

| Configuration | Required     | Default<br>(If not specified) | Type                   | Comments |
|---------------|--------------|-------------------------------|------------------------|----------|
| `blank=True`  | Optional     | `None`                        | `list[PkType] \| None` |          |
| `blank=False` | **Required** | `PydanticUndefined`           | `list[PkType] \| None` |          |

#### OneToOneRel
This field is created as a result of `OneToOneField` and is not directly configurable.

| Required | Default<br>(If not specified) | Type               | Comments |
|----------|-------------------------------|--------------------|----------|
| Optional | `None`                        | `[PkType] \| None` |          |
| Optional | `None`                        | `[PkType] \| None` |          |
| Optional | `None`                        | `[PkType] \| None` |          |
| Optional | `None`                        | `[PkType] \| None` |          |


#### ManyToOneRel, ManyToManyRel
These fields are created as a result of `ForeignKey`, `ManyToManyField` and are not directly configurable.

| Required | Default<br>(If not specified) | Type                   | Comments |
|----------|-------------------------------|------------------------|----------|
| Optional | `None`                        | `list[PkType] \| None` |          |
| Optional | `None`                        | `list[PkType] \| None` |          |
| Optional | `None`                        | `list[PkType] \| None` |          |
| Optional | `None`                        | `list[PkType] \| None` |          |
