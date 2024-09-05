
// Generated from Troiani.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "TroianiParser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by TroianiParser.
 */
class  TroianiListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterTermExpr(TroianiParser::TermExprContext *ctx) = 0;
  virtual void exitTermExpr(TroianiParser::TermExprContext *ctx) = 0;

  virtual void enterAddExpr(TroianiParser::AddExprContext *ctx) = 0;
  virtual void exitAddExpr(TroianiParser::AddExprContext *ctx) = 0;

  virtual void enterMulExpr(TroianiParser::MulExprContext *ctx) = 0;
  virtual void exitMulExpr(TroianiParser::MulExprContext *ctx) = 0;

  virtual void enterFactorExpr(TroianiParser::FactorExprContext *ctx) = 0;
  virtual void exitFactorExpr(TroianiParser::FactorExprContext *ctx) = 0;

  virtual void enterNumberExpr(TroianiParser::NumberExprContext *ctx) = 0;
  virtual void exitNumberExpr(TroianiParser::NumberExprContext *ctx) = 0;

  virtual void enterParenExpr(TroianiParser::ParenExprContext *ctx) = 0;
  virtual void exitParenExpr(TroianiParser::ParenExprContext *ctx) = 0;


};

