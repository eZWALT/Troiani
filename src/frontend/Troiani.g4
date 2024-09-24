/////////////////////////////////////////////////
//                                             //
//    Troiani - programming language grammar   //
//                                             //
/////////////////////////////////////////////////

grammar Troiani;

//////////////////////////////////////////////////
// Parser Rules                                 //
//////////////////////////////////////////////////

translation_unit: expr EOF
                ;

//R expressions evaluate to values/literals
r_expr  :  LPAR r_expr RPAR                     #parenthesis 
        |  identifier LBRK r_expr RBRK          #array_load
        |  identifier LPAR RPAR                 #call
        |  op=(NOT | PLUS | SUB) r_expr         #unary
        |  r_expr op=(EXP) r_expr               #exponentation
        |  r_expr op=(MUL | DIV | MOD) r_expr   #advanced_arith  
        |  r_expr op=(PLUS | SUB) r_expr        #simple_arith
        |  r_expr op=(EQ|NEQ|GT|GE|LT|LE) r_expr#relational 
        |  r_expr op=AND r_expr                 #logic
        |  r_expr op=OR  r_expr                 #logic  
        |  identifier                           #var_load
        ; 

//L expressions refer to variable loads (Memory access)
l_expr  : identifier
        ;

identifier: ID
          ;


//////////////////////////////////////////////////
// Lexer Rules                                  //
//////////////////////////////////////////////////

//ARITHMETIC OPERATORS
PLUS            : '+';
SUB             : '-';
MUL             : '*';
DIV             : '/';
MOD             : '%';
EXP             : '^';

//BOOLEAN OPERATORS 
LE              : '<=';
LT              : '<'; 
GE              : '>=';

//OTHER OPERATORS
ASSIGN          : ''


ID: ('a'..'z' | 'A'..'Z') ('a'..'z' | 'A'..'Z' | '_' | DIGIT);
  ;

fragment
DIGIT           : ('0'..'9');
INT_LIT         : DIGIT+; 
FLOAT_LIT       : ;
CHAR_LIT        : ;


