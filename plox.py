# Python lox version by hellgheast
import pathlib
import sys
from typing import List
from scanner import Scanner
import argparse


class Lox:
    """
    Main Lox interpreter logic
    """

    # TODO: Go for a static class ?
    def __init__(self):
        self.hadError: bool = False

    def report(self, line: int, where: str, msg: str) -> None:
        print(f"[line {line}] Error {where}: {msg}", file=sys.stderr)
        self.hadError = True

    def error(self, line: int, msg: str) -> None:
        self.report(line, "", msg)

    def run(self, source: str) -> None:
        scanner: Scanner = Scanner(self, source)
        tokens: List[str] = scanner.scanTokens()
        for token in tokens:
            print(token)

    def runFile(self, script_file: str) -> None:

        with open(script_file, "r") as f:
            print("Processing file..")
            program: str = f.read()
        self.run(program)
        if self.hadError:
            exit(65)

    def runPrompt(self) -> None:
        print("Launching prompt..")
        while True:
            try:
                read: str = input("> ")
                if read == "":
                    break
                else:
                    self.run(read)
                    self.hadError = False
            except EOFError as e:
                print("\n!! Exit !!")
                break
            except KeyboardInterrupt as e:
                print("\n!! Exit !!")
                break


if __name__ == "__main__":
    # developer: str = "Ismail"
    # print(f"Hello world {developer}")

    parser = argparse.ArgumentParser(
        description="Python lox interpreter", exit_on_error=False
    )
    parser.add_argument("--script", type=str, help="Path for a lox script file")
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        exit(64)
    # If we have an input script provider do something
    interpreter: Lox = Lox()
    if args.script:
        interpreter.runFile(args.script)
    else:
        interpreter.runPrompt()
