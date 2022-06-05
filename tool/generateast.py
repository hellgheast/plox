from io import TextIOWrapper
from typing import List
from pathlib import Path
import argparse


FOUR_SPACES: str = 4 * " "


def defineVisitInterface(file: TextIOWrapper, baseName: str, types: List[str]):
    """Implement visitor functions inside the Visitor class"""
    print(f"class Visitor:\n", file=file)
    for type in types:
        className: str = type.split(":")[0].strip()
        print(
            f"{FOUR_SPACES}def visit{className}{baseName}(self,{baseName.lower()}:{className}) -> Any:",
            file=file,
        )
        print(
            f'{2*FOUR_SPACES}raise NotImplementedError("Should be implemented")\n',
            file=file,
        )


def defineType(file: TextIOWrapper, baseName: str, className: str, classFields: str):
    # Class declaration
    print(f"class {className}({baseName}):", file=file)
    # Fields declaration

    # Fields declaration in the constructor
    fieldsList: str = ""
    fields: List[str] = classFields.split(",")
    for field in fields:
        fieldtype, name = field.strip().split(" ")
        fielddecl = name + ":" + fieldtype
        fieldsList += fielddecl + ","
    fieldsList = fieldsList[:-1]  # remove the last comma
    print(f"\n{FOUR_SPACES}def __init__(self,{fieldsList}):", file=file)
    # Write the content of the init part
    for field in fields:
        _, name = field.strip().split(" ")
        print(f"{2*FOUR_SPACES}self.{name} = {name}", file=file)
    print(f"\n{FOUR_SPACES}def accept(self,visitor:Visitor):", file=file)
    print(f"{2*FOUR_SPACES}return visitor.visit{className}{baseName}(self)", file=file)
    print("", file=file)


def defineAst(outputDir: str, baseName: str, types: List[str]):
    """Helper function to generator an AST file"""
    pathstr = str(Path(outputDir).joinpath(baseName.lower()).with_suffix(".py"))

    with open(pathstr, "w", encoding="utf-8") as f:

        print(
            "from __future__ import annotations\nfrom loxtoken import Token\nfrom typing import Any\n",
            file=f,
        )
        print(f"class {baseName}:", file=f)
        print(f"\n{FOUR_SPACES}def accept(self,visitor:Visitor) -> Any:", file=f)
        print(
            f'{2*FOUR_SPACES}raise NotImplementedError("Should be implemented")\n',
            file=f,
        )
        defineVisitInterface(f, baseName, types)
        for type in types:
            className: str = type.split(":")[0].strip()
            classFields: str = type.split(":")[1].strip()
            defineType(f, baseName, className, classFields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lox AST generator", exit_on_error=False
    )
    parser.add_argument("outputDir", type=str, help="Output directory for AST file")
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        exit(64)
    except SystemExit:
        # Is called when missing argument
        exit(64)

    defineAst(
        args.outputDir,
        "Expr",
        [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : object value",
            "Unary    : Token operator, Expr right",
        ],
    )
