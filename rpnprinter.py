from expr import Literal, Unary, Visitor, Binary, Grouping, Expr, Token
from loxtoken import TokenType


class RpnPrinter(Visitor):
    """Printer to show the nesting of the expression in RPN"""

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def rpntransform(self, name: str, *args: Expr):
        output: str = ""
        for expr in args:
            output += expr.accept(self) + " " 
        output += name
        return output

    # Implement the Visitor interface
    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.rpntransform(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.rpntransform("", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        # Not sure if this works..
        return self.rpntransform(expr.operator.lexeme, expr.right)


if __name__ == "__main__":

    # Test of the AstPrinter
    expression: Expr = Binary(
        Binary(
            Grouping(Literal(1)),
            Token(TokenType.PLUS,"+",None,1),
            Grouping(Literal(2)),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Binary(
            Grouping(Literal(4)),
            Token(TokenType.MINUS,"-",None,1),
            Grouping(Literal(3)),
        )        
    )

    print(RpnPrinter().print(expression))
