import pathlib
import click
from rich.traceback import install
from driver.python_d import PyRe
from driver.typesript_d import TsRe


# Включить перехват исключений
install(show_locals=True)


@click.command()
@click.option('inpath', "--ipath", '-i', type=click.Path(exists=True,
              file_okay=True, dir_okay=False, readable=True))
@click.option('opath', "--opath", '-o', type=click.Path(exists=True,
              file_okay=True, dir_okay=False, writable=True))
def greet(inpath: str, opath: str):
    if not inpath or not opath:
        raise ValueError(f"Не передан inpath или opath")
    pydantic_schema: pathlib.Path = pathlib.Path(inpath)
    out_typescript_schema: pathlib.Path = pathlib.Path(opath)
    res = PyRe.toUnion(pydantic_schema.read_text())
    res2 = TsRe.toSelf(res)
    # print(res2)
    out_typescript_schema.write_text(res2)
    print(f'Ok {out_typescript_schema}')


if __name__ == '__main__':
    greet()
    # greet(
    #     [
    #         '-i', '/media/denis/dd19b13d-bd85-46bb-8db9-5b8f6cf7a825/MyProject/pyjs/py/wbs/wbs_schema.py',
    #         '-o', '/media/denis/dd19b13d-bd85-46bb-8db9-5b8f6cf7a825/MyProject/vue_test/vts2/src/wbs/wbs_type.ts'
    #     ]
    # )
