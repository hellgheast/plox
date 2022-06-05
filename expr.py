from __future__ import annotations
from loxtoken import Token
from typing import Any

class Expr:

    def accept(self,visitor:Visitor) -> Any:
        raise NotImplementedError("Should be implemented")

class Visitor:

    def visitBinaryExpr(self,expr:Binary) -> Any:
        raise NotImplementedError("Should be implemented")

    def visitGroupingExpr(self,expr:Grouping) -> Any:
        raise NotImplementedError("Should be implemented")

    def visitLiteralExpr(self,expr:Literal) -> Any:
        raise NotImplementedError("Should be implemented")

    def visitUnaryExpr(self,expr:Unary) -> Any:
        raise NotImplementedError("Should be implemented")

class Binary(Expr):

    def __init__(self,left:Expr,operator:Token,right:Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self,visitor:Visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):

    def __init__(self,expression:Expr):
        self.expression = expression

    def accept(self,visitor:Visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):

    def __init__(self,value:object):
        self.value = value

    def accept(self,visitor:Visitor):
        return visitor.visitLiteralExpr(self)

class Unary(Expr):

    def __init__(self,operator:Token,right:Expr):
        self.operator = operator
        self.right = right

    def accept(self,visitor:Visitor):
        return visitor.visitUnaryExpr(self)

