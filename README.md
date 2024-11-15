# What

SuperSchema is a library that allows to define Pydantic schemas based on Django database models.

Similar libraries:
- [Djantic](https://jordaneremieff.github.io/djantic/)
- [Django Ninja Schema](https://django-ninja.dev/guides/response/django-pydantic/)
- [Ninja Schema](https://github.com/eadwinCode/ninja-schema)

# Why

SuperSchema is the most complete Pydantic schemas based on Django models.

# Key features

- Supports all Django model fields
- Supports all Django model relation fields:
    - ForeignKey, OneToOneField, ManyToManyField
    - The reverse relations of the above (ManyToOneRel, OneToOneRel, ManyToManyRel)
- Supports defining nested relations
- Provides as complete OpenAPI schema details as possible

# How

[See usage example here.](examples.ipynb)
