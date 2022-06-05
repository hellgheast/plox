from expr import Literal, Unary, Visitor, Binary, Grouping, Expr, Token
from loxtoken import TokenType


class AstPrinter(Visitor):
    """Printer to show the nesting of the expression"""

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *args: Expr):
        output: str = "("
        output += name
        for expr in args:
            output += " " + expr.accept(self)
        output += ")"
        return output

    # Implement the Visitor interface
    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


if __name__ == "__main__":

    # Test of the AstPrinter
    expression: Expr = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    print(AstPrinter().print(expression))
