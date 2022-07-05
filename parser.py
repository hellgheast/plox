from typing import List
from loxtoken import TokenType,Token
from expr import Binary, Expr, Grouping, Literal, Unary

class Parser:
    """Lox code parser
    We implement the grammar rules in a top-down/recursive desecent parser"""
    def __init__(self,tokens:List[Token]) -> None:
        # Flat sequences of tokens
        self.tokens: List[Token] = tokens
        # Current token
        self.current:int = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr:Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
            operator:Token = self.previous()
            right:Expr = self.comparison()
            expr = Binary(expr,operator,right)
        
        return expr

    def comparison(self) -> Expr:
        expr:Expr = self.term()

        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL):
            operator:Token = self.previous()
            right:Expr = self.term()
            expr = Binary(expr,operator,right)

        return expr

    def term(self) -> Expr:
        expr:Expr = self.factor()

        while self.match(TokenType.PLUS,TokenType.MINUS):
            operator:Token = self.previous()
            right:Expr = self.factor()
            expr = Binary(expr,operator,right)

        return expr        

    def factor(self) -> Expr:
        expr:Expr = self.unary()

        while self.match(TokenType.SLASH,TokenType.STAR):
            operator:Token = self.previous()
            right:Expr = self.unary()
            expr = Binary(expr,operator,right)

        return expr        

    def unary(self) -> Expr:
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator:Token = self.previous()
            right:Expr = self.unary()
            return Unary(operator,right)
        
        return self.primary()

    def primary(self) -> Expr:
        cur_token:TokenType = self.peek().type
        match cur_token:
            case TokenType.FALSE:
                self.advance()
                return Literal(False)
            case TokenType.TRUE:
                self.advance()
                return Literal(True)
            case TokenType.NIL:
                self.advance()
                return Literal(None)
            case TokenType.NUMBER | TokenType.STRING:
                self.advance()
                return Literal(self.previous().literal)
            case TokenType.LEFT_PAREN:
                self.advance()
                expr:Expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN,"Expect ')' after expression.")
                return Grouping(expr)

    #Continue on 6.3
    # Helper functions
    def match(self, *args:TokenType) -> bool:
        """Check if the current token matches any of the given TokenTypes"""
        for type in args:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self,type:TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
