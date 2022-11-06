import re

from base import BaseRe, OnlyInterface, OnlyInterface_args, UnionTypeObj, UnionTypeVal


class PyRe(BaseRe):
    # Поиск класса
    _find_class: re.Pattern = re.compile(
        '(class[\t ]+(?P<name>\\w+)[\t ]*)(?:\\((?P<parent>.+)\\))?:\n(?P<body>(?:\t+| {1,4}.*\n+)+)'
    )
    # Парсинг тела класса
    _find_elm_class: re.Pattern = re.compile(
        "(?P<doc>[\"']{3}\n(?:.\\s*(?![\"']{3}))+.[\"']{3})|(?P<comment>#.+\n)|(?P<enum>[\\w\\d_]+[\t ]*=[\t ]*.+\n)|(?P<class>[\\w\\d_]+[\t ]*\\:[\t ]*.+\n)"
    )
    # Парсинг строки с переменной
    _find_val: re.Pattern = re.compile(
        '(?P<name>[\\w\\d_]+)[\t ]*\\:?(?P<type_n>[\t ]*[^=\n]+)?[\t ]*=?(?P<val>.+)?'
    )

    @staticmethod
    def _toUnionTypeObj(text: str) -> UnionTypeObj:
        """
        Конвертировать Python типы объектов в универсальные
        """
        match text:
            case "Enum" | "enum.Enum": return UnionTypeObj.enum_t
            case "BaseModel" | 'pydantic.BaseModel': return UnionTypeObj.interface_t
            case _: return None

    @classmethod
    def _toUnionType(
            cls, text_type: str) -> list[tuple[UnionTypeVal, list[UnionTypeVal]]]:
        """
        Конвертировать Python типы значений в универсальные
        """
        if not text_type:
            return None
        res: list[tuple[UnionTypeVal, list[UnionTypeVal]]] = []
        for t in text_type.split('|'):
            match ''.join(t.split()):
                case "str": res.append(UnionTypeVal.str_t)
                case "int": res.append(UnionTypeVal.int_t)
                case "float": res.append(UnionTypeVal.float_t)
                case "bool": res.append(UnionTypeVal.bool_t)
                case "None": res.append(UnionTypeVal.none_t)
                case "list": res.append(UnionTypeVal.list_t)
                case "dict": res.append(UnionTypeVal.dict_t)
                case _ as r if d := re.search('list\\[([\\w\\d_]+)\\]', r):
                    res.append(
                        (
                            UnionTypeVal.list_d_t,
                            *[cls._toUnionType(x) for x in d.groups()]
                        )
                    )
                case _ as r:
                    print(f'PY Не найдено: {r}')
                    res.append(r)
        return res

    @ classmethod
    def toUnion(cls, text: str) -> list[OnlyInterface]:
        """
        Конвертировать Python в единый интерфейс
        """
        out_only_interface: list[OnlyInterface] = []
        # Найти классы Pydantic и Enum
        for r in cls._find_class.finditer(text):
            r: re.Regex
            o_document: str = ""
            o_arg_s: list[OnlyInterface_args] = []
            type_r: UnionTypeObj = cls._toUnionTypeObj(r['parent'])
            if not type_r:
                continue
            for r2 in cls._find_elm_class.finditer(r['body']):
                r2: re.Regex
                o_arg: OnlyInterface_args = {}
                match r2.groupdict():
                    case {"doc": doc_} if doc_:
                        # Обрезаем кавычки
                        o_document = re.sub('''^["']{3}|["']{3}$''', '', doc_)
                        continue
                    case {'comment': comment} if comment:
                        o_arg['comment'] = re.sub('^#', '', comment)
                    case {'enum': enum_} if enum_:
                        n, t, v = cls._find_val.search(enum_).groups()
                        o_arg['name'] = n
                        o_arg['value'] = v
                        o_arg['type_a'] = cls._toUnionType(t)
                    case {'class': class_} if class_:
                        n, t, v = cls._find_val.search(class_).groups()
                        o_arg['name'] = n
                        o_arg['value'] = v
                        o_arg['type_a'] = cls._toUnionType(t)
                    case _:
                        raise ValueError("Не найдено")
                o_arg_s.append(o_arg)
            out_only_interface.append(
                OnlyInterface(
                    type_r=type_r,
                    name=r['name'],
                    doc=o_document,
                    args=o_arg_s
                )
            )
        return out_only_interface
