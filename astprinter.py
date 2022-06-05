from typing import List
from expr import Literal, Unary, Visitor, Binary, Grouping, Expr


class AstPrint(Visitor):
    """Printer to show the nesting of the expression"""

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self,name:str,*args:Expr):
        output:str = "("
        output += name
        for expr in args:
            output += " " + expr.accept(self)
        output += ")"
        return output

    # Implement the Visitor interface
    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self, expr:Grouping) -> str:
        return self.parenthesize("group",expr.expression)
    
    def visitLiteralExpr(self, expr:Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visitUnaryExpr(self,expr:Unary) -> str:
        return self.parenthesize(expr.operator.lexeme,expr.right)