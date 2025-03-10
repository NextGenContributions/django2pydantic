![PyPI - License](https://img.shields.io/pypi/l/django2pydantic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django2pydantic)

# Why

django2pydantic serves as a bridge between Django models and Pydantic schemas, allowing you to easily convert Django models into Pydantic schemas. This is particularly useful when building APIs with Django and Django Ninja, as it allows you to use Pydantic schemas for request and response validation, serialization, and documentation.

# What

django2pydantic is a library that enables you to generate Pydantic schemas based on Django database models.

Similar libraries:

- [Djantic](https://jordaneremieff.github.io/djantic/)
- [Django Ninja Schema](https://django-ninja.dev/guides/response/django-pydantic/)
- [Ninja Schema](https://github.com/eadwinCode/ninja-schema)

## Integration with Django Ninja CRUDL

Our other project [django-ninja-crudl](https://github.com/NextGenContributions/django-ninja-crudl) uses django2pydantic as its foundation for generating Pydantic schemas from Django models, providing an efficient way to implement CRUDL operations in your Django Ninja APIs.

## Alternative to Django Ninja's ModelSchema

Django2pydantic serves as a more complete alternative to [Django Ninja's ModelSchema](https://django-ninja.dev/guides/response/django-pydantic/) which is shipped with Django Ninja. While Django Ninja provides basic model schema conversion functionality, django2pydantic offers more comprehensive features:

- Full support for all Django field types instead of just the basic ones
- Proper handling of model properties and methods
- Enhanced support for complex relationship fields (including reverse relations)
- More detailed and accurate OpenAPI schema generation
- Greater flexibility in defining nested relations and customizing schema output

This makes django2pydantic particularly useful for projects with complex models and relationship structures where the built-in `ModelSchema` may fall short.

## Key features

- Supports all Django model field types
- Supports @property decorated Django model methods
- Supports all Django model relation fields:
  - ForeignKey, OneToOneField, ManyToManyField
  - The reverse relations of the above (ManyToOneRel, OneToOneRel, ManyToManyRel)
- Supports defining nested relations
- Provides as complete OpenAPI schema details as possible

# How to use

See [usage examples here](tests/examples.ipynb).
