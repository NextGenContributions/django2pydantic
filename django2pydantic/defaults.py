"""Default field type handlers for django2pydantic."""

from django2pydantic import handlers
from django2pydantic.registry import FieldTypeRegistry

field_type_registry: FieldTypeRegistry = FieldTypeRegistry.instance()
field_type_registry.register(handlers.CharFieldHandler)
field_type_registry.register(handlers.TextFieldHandler)
field_type_registry.register(handlers.UUIDFieldHandler)
field_type_registry.register(handlers.EmailFieldHandler)
field_type_registry.register(handlers.JSONFieldHandler)
field_type_registry.register(handlers.GenericIpAddressFieldHandler)
field_type_registry.register(handlers.DecimalFieldHandler)
field_type_registry.register(handlers.ForeignKeyHandler)
field_type_registry.register(handlers.FloatFieldHandler)
field_type_registry.register(handlers.SmallAutoFieldHandler)
field_type_registry.register(handlers.IntegerFieldHandler)
field_type_registry.register(handlers.SmallIntegerFieldHandler)
field_type_registry.register(handlers.PositiveSmallIntegerFieldHandler)
field_type_registry.register(handlers.PositiveIntegerFieldHandler)
field_type_registry.register(handlers.PositiveBigIntegerFieldHandler)
field_type_registry.register(handlers.TimeFieldHandler)
field_type_registry.register(handlers.DateFieldHandler)
field_type_registry.register(handlers.DateTimeFieldHandler)
field_type_registry.register(handlers.DurationFieldHandler)
field_type_registry.register(handlers.BinaryFieldHandler)
field_type_registry.register(handlers.BooleanFieldHandler)
field_type_registry.register(handlers.FileFieldHandler)
field_type_registry.register(handlers.FilePathFieldHandler)
field_type_registry.register(handlers.ImageFieldHandler)
field_type_registry.register(handlers.UrlFieldHandler)
field_type_registry.register(handlers.BigIntegerFieldHandler)
field_type_registry.register(handlers.SlugFieldHandler)
field_type_registry.register(handlers.AutoFieldHandler)
field_type_registry.register(handlers.BigAutoFieldHandler)
field_type_registry.register(handlers.PropertyHandler)
field_type_registry.register(handlers.OneToOneFieldHandler)
field_type_registry.register(handlers.ManyToManyFieldHandler)
field_type_registry.register(handlers.ManyToManyRelHandler)
