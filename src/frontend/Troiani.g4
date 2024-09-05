grammar Troiani;


// Lexer rules
NUMBER  : [0-9]+ ;
PLUS    : '+' ;
MUL     : '*' ;
LPAREN  : '(' ;
RPAREN  : ')' ;
WS      : [ \t\r\n]+ -> skip ;

// Parser rules
expr    : expr PLUS term      # AddExpr
        | term                # TermExpr
        ;

term    : term MUL factor     # MulExpr
        | factor              # FactorExpr
        ;

factor  : NUMBER              # NumberExpr
        | LPAREN expr RPAREN  # ParenExpr
        ;