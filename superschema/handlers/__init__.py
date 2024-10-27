"""All field type handlers."""

from superschema.handlers.auto import (
    AutoFieldHandler,
    BigAutoFieldHandler,
    SmallAutoFieldHandler,
)
from superschema.handlers.base import FieldTypeHandler
from superschema.handlers.boolean import BooleanFieldHandler
from superschema.handlers.file import (
    BinaryFieldHandler,
    FileFieldHandler,
    FilePathFieldHandler,
    ImageFieldHandler,
)
from superschema.handlers.json import JSONFieldHandler
from superschema.handlers.network import GenericIpAddressFieldHandler
from superschema.handlers.numbers import (
    BigIntegerFieldHandler,
    DecimalFieldHandler,
    FloatFieldHandler,
    IntegerFieldHandler,
    PositiveBigIntegerFieldHandler,
    PositiveIntegerFieldHandler,
    PositiveSmallIntegerFieldHandler,
    SmallIntegerFieldHandler,
)
from superschema.handlers.property import PropertyHandler
from superschema.handlers.relational import (
    ForeignKeyHandler,
    ManyToManyFieldHandler,
    OneToOneFieldHandler,
)
from superschema.handlers.text import (
    CharFieldHandler,
    EmailFieldHandler,
    SlugFieldHandler,
    TextFieldHandler,
    UrlFieldHandler,
    UUIDFieldHandler,
)
from superschema.handlers.time import (
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
