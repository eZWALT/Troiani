
// Generated from Troiani.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "TroianiListener.h"


/**
 * This class provides an empty implementation of TroianiListener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  TroianiBaseListener : public TroianiListener {
public:

  virtual void enterTermExpr(TroianiParser::TermExprContext * /*ctx*/) override { }
  virtual void exitTermExpr(TroianiParser::TermExprContext * /*ctx*/) override { }

  virtual void enterAddExpr(TroianiParser::AddExprContext * /*ctx*/) override { }
  virtual void exitAddExpr(TroianiParser::AddExprContext * /*ctx*/) override { }

  virtual void enterMulExpr(TroianiParser::MulExprContext * /*ctx*/) override { }
  virtual void exitMulExpr(TroianiParser::MulExprContext * /*ctx*/) override { }

  virtual void enterFactorExpr(TroianiParser::FactorExprContext * /*ctx*/) override { }
  virtual void exitFactorExpr(TroianiParser::FactorExprContext * /*ctx*/) override { }

  virtual void enterNumberExpr(TroianiParser::NumberExprContext * /*ctx*/) override { }
  virtual void exitNumberExpr(TroianiParser::NumberExprContext * /*ctx*/) override { }

  virtual void enterParenExpr(TroianiParser::ParenExprContext * /*ctx*/) override { }
  virtual void exitParenExpr(TroianiParser::ParenExprContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

