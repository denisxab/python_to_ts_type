import datetime
import re

from base import BaseRe
from base import BaseRe, OnlyInterface, OnlyInterface_args, UnionTypeObj, UnionTypeVal


class TsRe(BaseRe):
    find_class: re.Pattern = ''

    @classmethod
    def fromUnionTypeVal(
            cls, type_v_u: list[UnionTypeVal]) -> list[tuple[UnionTypeVal, list[UnionTypeVal]]]:
        """
        Конвертировать из универсального типа в типы TypeScript
        """
        res = []
        for t in type_v_u:
            match t:
                case UnionTypeVal.str_t: res.append('string')
                case UnionTypeVal.int_t: res.append('number')
                case UnionTypeVal.float_t: res.append('number')
                case UnionTypeVal.bool_t: res.append('boolean')
                case UnionTypeVal.none_t: res.append('undefined')
                case UnionTypeVal.list_t: res.append('any[]')
                case UnionTypeVal.dict_t: res.append('object')
                case UnionTypeVal.any_t as r: res.append(r)
                case _ as r if r[0] == UnionTypeVal.list_d_t: res.append(f'{cls.fromUnionTypeVal([r[1][0]])[0]}[]')
                case _ as r:
                    print(f'TS Не найдено: {r}')
                    res.append(r)
        return res

    @ classmethod
    def toSelf(cls, only_interface: list[OnlyInterface]):
        """
        Конвертировать единый интерфейс в TypeScript
        """
        tmp = []

        for i in only_interface:
            i: OnlyInterface
            type_obj: str = ''
            match i.type_r:
                case UnionTypeObj.enum_t:
                    tmp.append('export enum ')
                    type_obj = UnionTypeObj.enum_t
                case UnionTypeObj.interface_t:
                    tmp.append('export interface ')
                    type_obj = UnionTypeObj.interface_t
                case _:
                    raise ValueError("Не найдено")
            tmp.append(f"{i.name}" + "{\n")
            tmp.append(f"/*AUTO_GEN:{datetime.datetime.now()}\n{i.doc}\t\n*/")
            for a in i.args:
                match a:
                    case {'comment': comment_}:
                        tmp.append(f'\n\t// {comment_}')
                    case {"name": name, "value": value, "type_a": type_a}:
                        match type_obj:
                            case UnionTypeObj.enum_t:
                                tmp.append(
                                    f"\t{name}{':'+'|'.join(cls.fromUnionTypeVal(type_a)) if type_a else ''}{' = '+value if value else ''},"
                                )
                            case UnionTypeObj.interface_t:
                                tmp.append(
                                    f"\t{name}{':'+'|'.join(cls.fromUnionTypeVal(type_a)) if type_a else ''}{' = '+value if value else ''};"
                                )
            tmp.append("\n}\n")
        return ''.join(tmp)
