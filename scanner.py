from typing import List

from loxtoken import LoxKeyword, Token, TokenType


class Scanner:
    def __init__(self, lox, source: str):
        self.source: str = source
        self.lox = lox
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self) -> None:
        char = self.advance()
        match char:
            # TODO: Refactor with nice pattern matching features
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)
            case "!":
                token = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                self.addToken(token)
            case "=":
                token = TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                self.addToken(token)
            case "<":
                token = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.addToken(token)
            case ">":
                token = (
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
                self.addToken(token)
            case "/":
                if self.match("/"):
                    # We're dealing with a comment
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                elif self.match("*"):
                    # We're dealing with C-like comment
                    self.handleBlockComments()
                else:
                    # We're dealing with a division
                    self.addToken(TokenType.SLASH)
            case " " | "\r" | "\t":
                # We don't care about whitespaces
                pass
            case "\n":
                self.line += 1
            case '"':
                self.handleString()
            case _:
                if self.isDigit(char):
                    self.handleNumber()
                elif self.isAlpha(char):
                    self.handleIdentifier()
                else:
                    # TODO: Continue at 4.6.2
                    self.lox.error(self.line, "Unexpected character")

    def isDigit(self, current_char: str) -> bool:
        return current_char >= "0" and current_char <= "9"

    def isAlpha(self, current_char: str) -> bool:
        return (
            (current_char >= "a" and current_char <= "z")
            or (current_char >= "A" and current_char <= "Z")
            or current_char == "_"
        )

    def isAlphaNumeric(self, current_char: str) -> bool:
        return self.isAlpha(current_char) or self.isDigit(current_char)

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        """Return the current char and advance to next char"""
        char: str = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected: str) -> bool:
        """Check if the current char is the expected one and advance to the next char"""
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        """Return the current char"""
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self) -> str:
        """Return the next char"""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def handleNumber(self) -> None:

        # Integer part
        while self.isDigit(self.peek()):
            self.advance()
        
        #TODO Add support for pure integers and floating points

        # Check the fractional part
        if self.peek() == "." and self.isDigit(self.peekNext()):
            # Consume the dot
            self.advance()

        # Fractional part
        while self.isDigit(self.peek()):
            self.advance()

        # Finished the parsing of the number
        self.addTokenObj(
            TokenType.NUMBER, float(self.source[self.start : self.current])
        )

    def handleString(self) -> None:
        # Move the current pointer until end of string
        while (peeked := self.peek()) != '"' and not self.isAtEnd():
            if peeked == "\n":
                self.line += 1
            self.advance()

        if self.isAtEnd():
            self.lox.error(self.line, "Unterminated string")
            return

        self.advance()

        string_value: str = self.source[self.start + 1 : self.current - 1]
        self.addTokenObj(TokenType.STRING, string_value)

    def handleIdentifier(self) -> None:
        # Find identifier and advance until end of indentifier
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        # Might be a given keyword or just identifier
        text: str = self.source[self.start : self.current]
        tokenType: TokenType = LoxKeyword.get(text)
        if tokenType is None:
            # If no given keyword is find we define it as an identifier
            tokenType = TokenType.IDENTIFIER

        self.addToken(tokenType)

    def handleBlockComments(self) -> None:
        level = 1

        while level != 0 and not self.isAtEnd():
            peeked = self.peek()
            nextpeeked = self.peekNext()
            # Handling newlines and multiples levels of comments
            if peeked == "\n":
                self.line += 1
            if peeked == "/" and nextpeeked == "*":
                level += 1
                self.advance()
                self.advance()
            elif peeked == "*" and nextpeeked == "/":
                level -= 1
                self.advance()
                self.advance()
            else:
                self.advance()

        # TODO: Check if we finished to handle the comments
        if self.isAtEnd() and level > 0:
            self.lox.error(self.line, "Unterminated block comment")
            return

    def addToken(self, type: TokenType) -> None:
        self.addTokenObj(type, None)

    def addTokenObj(self, type: TokenType, obj: object) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, obj, self.line))
