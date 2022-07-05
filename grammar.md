# Precedence rules (from higher to lower priority)

| Name        | Operators   | Associates |
| ----------- | ----------- | ---------- |
| Unary       | ! -         | Right      |
| Factor      | / *         | Left       |
| Term        | - +         | Left       |
| Comparison  | > >= < <=   | Left       |
| Equality    | == !=       | Left       |   

# Language grammar (for precedence levels)
We encode in the grammar the precendence rules.

* expression -> equality
* equality   -> comparison (("=="|"!=") comparison )*;
* comparison -> term ((">"|">="|"<"|"<=") term)  *;
* term -> factor (("+" | "-") factor ) *;
* factor -> unary (("/" | "*") unary ) *;
* unary -> ("!" | "-" ) unary | primary ;
* primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
