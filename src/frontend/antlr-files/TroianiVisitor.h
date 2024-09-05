
// Generated from Troiani.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "TroianiParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by TroianiParser.
 */
class  TroianiVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by TroianiParser.
   */
    virtual antlrcpp::Any visitTermExpr(TroianiParser::TermExprContext *context) = 0;

    virtual antlrcpp::Any visitAddExpr(TroianiParser::AddExprContext *context) = 0;

    virtual antlrcpp::Any visitMulExpr(TroianiParser::MulExprContext *context) = 0;

    virtual antlrcpp::Any visitFactorExpr(TroianiParser::FactorExprContext *context) = 0;

    virtual antlrcpp::Any visitNumberExpr(TroianiParser::NumberExprContext *context) = 0;

    virtual antlrcpp::Any visitParenExpr(TroianiParser::ParenExprContext *context) = 0;


};

