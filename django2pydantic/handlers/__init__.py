"""All field type handlers."""

from django2pydantic.handlers.auto import (
    AutoFieldHandler,
    BigAutoFieldHandler,
    SmallAutoFieldHandler,
)
from django2pydantic.handlers.base import FieldTypeHandler
from django2pydantic.handlers.boolean import BooleanFieldHandler
from django2pydantic.handlers.file import (
    BinaryFieldHandler,
    FileFieldHandler,
    FilePathFieldHandler,
    ImageFieldHandler,
)
from django2pydantic.handlers.json import JSONFieldHandler
from django2pydantic.handlers.network import GenericIpAddressFieldHandler
from django2pydantic.handlers.numbers import (
    BigIntegerFieldHandler,
    DecimalFieldHandler,
    FloatFieldHandler,
    IntegerFieldHandler,
    PositiveBigIntegerFieldHandler,
    PositiveIntegerFieldHandler,
    PositiveSmallIntegerFieldHandler,
    SmallIntegerFieldHandler,
)
from django2pydantic.handlers.property import PropertyHandler
from django2pydantic.handlers.relational import (
    ForeignKeyHandler,
    ManyToManyFieldHandler,
    OneToOneFieldHandler,
)
from django2pydantic.handlers.text import (
    CharFieldHandler,
    EmailFieldHandler,
    SlugFieldHandler,
    TextFieldHandler,
    UrlFieldHandler,
    UUIDFieldHandler,
)
from django2pydantic.handlers.time import (
    DateFieldHandler,
    DateTimeFieldHandler,
    DurationFieldHandler,
    TimeFieldHandler,
)

__all__: list[str] = [
    "FieldTypeHandler",
    "BooleanFieldHandler",
    "GenericIpAddressFieldHandler",
    "BigIntegerFieldHandler",
    "DecimalFieldHandler",
    "FloatFieldHandler",
    "IntegerFieldHandler",
    "PositiveBigIntegerFieldHandler",
    "PositiveIntegerFieldHandler",
    "PositiveSmallIntegerFieldHandler",
    "SmallAutoFieldHandler",
    "SmallIntegerFieldHandler",
    "PropertyHandler",
    "CharFieldHandler",
    "EmailFieldHandler",
    "TextFieldHandler",
    "UUIDFieldHandler",
    "DateFieldHandler",
    "DateTimeFieldHandler",
    "DurationFieldHandler",
    "TimeFieldHandler",
    "AutoFieldHandler",
    "BigAutoFieldHandler",
    "ForeignKeyHandler",
    "OneToOneFieldHandler",
    "ManyToManyFieldHandler",
    "PropertyHandler",
    "JSONFieldHandler",
    "BinaryFieldHandler",
    "FileFieldHandler",
    "FilePathFieldHandler",
    "ImageFieldHandler",
    "UrlFieldHandler",
    "SlugFieldHandler",
]
