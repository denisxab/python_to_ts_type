import abc
from enum import Enum
import typing


class UnionTypeVal(Enum):
    """
    Стандартные типы
    """
    str_t = "str_t"
    int_t = "int_t"
    float_t = "float_t"
    bool_t = "bool_t"
    none_t = "none_t"
    list_t = "list_t"
    list_d_t = "list_d_t"
    dict_t = "dict_t"
    any_t = "any_t"


class UnionTypeObj(Enum):
    """
    Стандартные объекты
    """
    enum_t = "enum_t"
    interface_t = "interface_t"


class OnlyInterface_args(typing.TypedDict):
    # Комментарий
    comment: str
    # Имя
    name: str
    # Тип переменной, может быть несколько типов. Например для `str | int |
    # float`
    type_a: list[
        tuple[
            UnionTypeVal,
            # Дополнительные типы. Например для `list[str]`
            list[UnionTypeVal]
        ]
    ]
    # Значение
    value: str


class OnlyInterface(typing.NamedTuple):
    # Имя
    name: str
    # Тип объекта
    type_r: UnionTypeObj
    # Документация
    doc: str
    # Аргументы
    args: list[OnlyInterface_args]


class BaseRe(abc.ABC):
    """Базовый класс для конвертации языка"""
    @staticmethod
    def _toUnionTypeObj(text: str) -> UnionTypeObj: ...

    @staticmethod
    def _toUnionType(text_type: str) -> UnionTypeVal: ...

    @classmethod
    def toUnion(cls, text: str) -> list[OnlyInterface]: ...

    @classmethod
    def toSelf(cls, only_interface: list[OnlyInterface]): ...
