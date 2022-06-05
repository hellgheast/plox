from enum import Enum, auto
from typing import Dict


class TokenType(Enum):
    """
    Using the Enum class for assigning the name of a lox token to a value
    """

    # Single char tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    # One or two char tokens
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"
    EOF = auto()

    def __str__(self):
        return self.name


LoxKeyword: Dict[str, TokenType] = {
    # Keyword dict
    TokenType.AND.value: TokenType.AND,
    TokenType.CLASS.value: TokenType.CLASS,
    TokenType.ELSE.value: TokenType.ELSE,
    TokenType.FALSE.value: TokenType.FALSE,
    TokenType.FOR.value: TokenType.FOR,
    TokenType.FUN.value: TokenType.FUN,
    TokenType.IF.value: TokenType.IF,
    TokenType.NIL.value: TokenType.NIL,
    TokenType.OR.value: TokenType.OR,
    TokenType.PRINT.value: TokenType.PRINT,
    TokenType.RETURN.value: TokenType.RETURN,
    TokenType.SUPER.value: TokenType.SUPER,
    TokenType.THIS.value: TokenType.THIS,
    TokenType.TRUE.value: TokenType.TRUE,
    TokenType.VAR.value: TokenType.VAR,
    TokenType.WHILE.value: TokenType.WHILE,
}


class Token:
    """
    Placeholder class that contains all the info for a given Token
    """

    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
