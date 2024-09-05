
// Generated from Troiani.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "TroianiVisitor.h"


/**
 * This class provides an empty implementation of TroianiVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  TroianiBaseVisitor : public TroianiVisitor {
public:

  virtual antlrcpp::Any visitTermExpr(TroianiParser::TermExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitAddExpr(TroianiParser::AddExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitMulExpr(TroianiParser::MulExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitFactorExpr(TroianiParser::FactorExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNumberExpr(TroianiParser::NumberExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParenExpr(TroianiParser::ParenExprContext *ctx) override {
    return visitChildren(ctx);
  }


};

