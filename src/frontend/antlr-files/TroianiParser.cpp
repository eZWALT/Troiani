
// Generated from Troiani.g4 by ANTLR 4.7.2


#include "TroianiVisitor.h"

#include "TroianiParser.h"


using namespace antlrcpp;
using namespace antlr4;

TroianiParser::TroianiParser(TokenStream *input) : Parser(input) {
  _interpreter = new atn::ParserATNSimulator(this, _atn, _decisionToDFA, _sharedContextCache);
}

TroianiParser::~TroianiParser() {
  delete _interpreter;
}

std::string TroianiParser::getGrammarFileName() const {
  return "Troiani.g4";
}

const std::vector<std::string>& TroianiParser::getRuleNames() const {
  return _ruleNames;
}

dfa::Vocabulary& TroianiParser::getVocabulary() const {
  return _vocabulary;
}


//----------------- ExprContext ------------------------------------------------------------------

TroianiParser::ExprContext::ExprContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t TroianiParser::ExprContext::getRuleIndex() const {
  return TroianiParser::RuleExpr;
}

void TroianiParser::ExprContext::copyFrom(ExprContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- TermExprContext ------------------------------------------------------------------

TroianiParser::TermContext* TroianiParser::TermExprContext::term() {
  return getRuleContext<TroianiParser::TermContext>(0);
}

TroianiParser::TermExprContext::TermExprContext(ExprContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::TermExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitTermExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AddExprContext ------------------------------------------------------------------

TroianiParser::ExprContext* TroianiParser::AddExprContext::expr() {
  return getRuleContext<TroianiParser::ExprContext>(0);
}

tree::TerminalNode* TroianiParser::AddExprContext::PLUS() {
  return getToken(TroianiParser::PLUS, 0);
}

TroianiParser::TermContext* TroianiParser::AddExprContext::term() {
  return getRuleContext<TroianiParser::TermContext>(0);
}

TroianiParser::AddExprContext::AddExprContext(ExprContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::AddExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitAddExpr(this);
  else
    return visitor->visitChildren(this);
}

TroianiParser::ExprContext* TroianiParser::expr() {
   return expr(0);
}

TroianiParser::ExprContext* TroianiParser::expr(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  TroianiParser::ExprContext *_localctx = _tracker.createInstance<ExprContext>(_ctx, parentState);
  TroianiParser::ExprContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 0;
  enterRecursionRule(_localctx, 0, TroianiParser::RuleExpr, precedence);

    

  auto onExit = finally([=] {
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    _localctx = _tracker.createInstance<TermExprContext>(_localctx);
    _ctx = _localctx;
    previousContext = _localctx;

    setState(7);
    term(0);
    _ctx->stop = _input->LT(-1);
    setState(14);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 0, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        auto newContext = _tracker.createInstance<AddExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
        _localctx = newContext;
        pushNewRecursionContext(newContext, startState, RuleExpr);
        setState(9);

        if (!(precpred(_ctx, 2))) throw FailedPredicateException(this, "precpred(_ctx, 2)");
        setState(10);
        match(TroianiParser::PLUS);
        setState(11);
        term(0); 
      }
      setState(16);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 0, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- TermContext ------------------------------------------------------------------

TroianiParser::TermContext::TermContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t TroianiParser::TermContext::getRuleIndex() const {
  return TroianiParser::RuleTerm;
}

void TroianiParser::TermContext::copyFrom(TermContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- MulExprContext ------------------------------------------------------------------

TroianiParser::TermContext* TroianiParser::MulExprContext::term() {
  return getRuleContext<TroianiParser::TermContext>(0);
}

tree::TerminalNode* TroianiParser::MulExprContext::MUL() {
  return getToken(TroianiParser::MUL, 0);
}

TroianiParser::FactorContext* TroianiParser::MulExprContext::factor() {
  return getRuleContext<TroianiParser::FactorContext>(0);
}

TroianiParser::MulExprContext::MulExprContext(TermContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::MulExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitMulExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- FactorExprContext ------------------------------------------------------------------

TroianiParser::FactorContext* TroianiParser::FactorExprContext::factor() {
  return getRuleContext<TroianiParser::FactorContext>(0);
}

TroianiParser::FactorExprContext::FactorExprContext(TermContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::FactorExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitFactorExpr(this);
  else
    return visitor->visitChildren(this);
}

TroianiParser::TermContext* TroianiParser::term() {
   return term(0);
}

TroianiParser::TermContext* TroianiParser::term(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  TroianiParser::TermContext *_localctx = _tracker.createInstance<TermContext>(_ctx, parentState);
  TroianiParser::TermContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 2;
  enterRecursionRule(_localctx, 2, TroianiParser::RuleTerm, precedence);

    

  auto onExit = finally([=] {
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    _localctx = _tracker.createInstance<FactorExprContext>(_localctx);
    _ctx = _localctx;
    previousContext = _localctx;

    setState(18);
    factor();
    _ctx->stop = _input->LT(-1);
    setState(25);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 1, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        auto newContext = _tracker.createInstance<MulExprContext>(_tracker.createInstance<TermContext>(parentContext, parentState));
        _localctx = newContext;
        pushNewRecursionContext(newContext, startState, RuleTerm);
        setState(20);

        if (!(precpred(_ctx, 2))) throw FailedPredicateException(this, "precpred(_ctx, 2)");
        setState(21);
        match(TroianiParser::MUL);
        setState(22);
        factor(); 
      }
      setState(27);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 1, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- FactorContext ------------------------------------------------------------------

TroianiParser::FactorContext::FactorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t TroianiParser::FactorContext::getRuleIndex() const {
  return TroianiParser::RuleFactor;
}

void TroianiParser::FactorContext::copyFrom(FactorContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- NumberExprContext ------------------------------------------------------------------

tree::TerminalNode* TroianiParser::NumberExprContext::NUMBER() {
  return getToken(TroianiParser::NUMBER, 0);
}

TroianiParser::NumberExprContext::NumberExprContext(FactorContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::NumberExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitNumberExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ParenExprContext ------------------------------------------------------------------

tree::TerminalNode* TroianiParser::ParenExprContext::LPAREN() {
  return getToken(TroianiParser::LPAREN, 0);
}

TroianiParser::ExprContext* TroianiParser::ParenExprContext::expr() {
  return getRuleContext<TroianiParser::ExprContext>(0);
}

tree::TerminalNode* TroianiParser::ParenExprContext::RPAREN() {
  return getToken(TroianiParser::RPAREN, 0);
}

TroianiParser::ParenExprContext::ParenExprContext(FactorContext *ctx) { copyFrom(ctx); }

antlrcpp::Any TroianiParser::ParenExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<TroianiVisitor*>(visitor))
    return parserVisitor->visitParenExpr(this);
  else
    return visitor->visitChildren(this);
}
TroianiParser::FactorContext* TroianiParser::factor() {
  FactorContext *_localctx = _tracker.createInstance<FactorContext>(_ctx, getState());
  enterRule(_localctx, 4, TroianiParser::RuleFactor);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(33);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case TroianiParser::NUMBER: {
        _localctx = dynamic_cast<FactorContext *>(_tracker.createInstance<TroianiParser::NumberExprContext>(_localctx));
        enterOuterAlt(_localctx, 1);
        setState(28);
        match(TroianiParser::NUMBER);
        break;
      }

      case TroianiParser::LPAREN: {
        _localctx = dynamic_cast<FactorContext *>(_tracker.createInstance<TroianiParser::ParenExprContext>(_localctx));
        enterOuterAlt(_localctx, 2);
        setState(29);
        match(TroianiParser::LPAREN);
        setState(30);
        expr(0);
        setState(31);
        match(TroianiParser::RPAREN);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool TroianiParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 0: return exprSempred(dynamic_cast<ExprContext *>(context), predicateIndex);
    case 1: return termSempred(dynamic_cast<TermContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool TroianiParser::exprSempred(ExprContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 2);

  default:
    break;
  }
  return true;
}

bool TroianiParser::termSempred(TermContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 1: return precpred(_ctx, 2);

  default:
    break;
  }
  return true;
}

// Static vars and initialization.
std::vector<dfa::DFA> TroianiParser::_decisionToDFA;
atn::PredictionContextCache TroianiParser::_sharedContextCache;

// We own the ATN which in turn owns the ATN states.
atn::ATN TroianiParser::_atn;
std::vector<uint16_t> TroianiParser::_serializedATN;

std::vector<std::string> TroianiParser::_ruleNames = {
  "expr", "term", "factor"
};

std::vector<std::string> TroianiParser::_literalNames = {
  "", "", "'+'", "'*'", "'('", "')'"
};

std::vector<std::string> TroianiParser::_symbolicNames = {
  "", "NUMBER", "PLUS", "MUL", "LPAREN", "RPAREN", "WS"
};

dfa::Vocabulary TroianiParser::_vocabulary(_literalNames, _symbolicNames);

std::vector<std::string> TroianiParser::_tokenNames;

TroianiParser::Initializer::Initializer() {
	for (size_t i = 0; i < _symbolicNames.size(); ++i) {
		std::string name = _vocabulary.getLiteralName(i);
		if (name.empty()) {
			name = _vocabulary.getSymbolicName(i);
		}

		if (name.empty()) {
			_tokenNames.push_back("<INVALID>");
		} else {
      _tokenNames.push_back(name);
    }
	}

  _serializedATN = {
    0x3, 0x608b, 0xa72a, 0x8133, 0xb9ed, 0x417c, 0x3be7, 0x7786, 0x5964, 
    0x3, 0x8, 0x26, 0x4, 0x2, 0x9, 0x2, 0x4, 0x3, 0x9, 0x3, 0x4, 0x4, 0x9, 
    0x4, 0x3, 0x2, 0x3, 0x2, 0x3, 0x2, 0x3, 0x2, 0x3, 0x2, 0x3, 0x2, 0x7, 
    0x2, 0xf, 0xa, 0x2, 0xc, 0x2, 0xe, 0x2, 0x12, 0xb, 0x2, 0x3, 0x3, 0x3, 
    0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x7, 0x3, 0x1a, 0xa, 0x3, 
    0xc, 0x3, 0xe, 0x3, 0x1d, 0xb, 0x3, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 
    0x4, 0x3, 0x4, 0x5, 0x4, 0x24, 0xa, 0x4, 0x3, 0x4, 0x2, 0x4, 0x2, 0x4, 
    0x5, 0x2, 0x4, 0x6, 0x2, 0x2, 0x2, 0x25, 0x2, 0x8, 0x3, 0x2, 0x2, 0x2, 
    0x4, 0x13, 0x3, 0x2, 0x2, 0x2, 0x6, 0x23, 0x3, 0x2, 0x2, 0x2, 0x8, 0x9, 
    0x8, 0x2, 0x1, 0x2, 0x9, 0xa, 0x5, 0x4, 0x3, 0x2, 0xa, 0x10, 0x3, 0x2, 
    0x2, 0x2, 0xb, 0xc, 0xc, 0x4, 0x2, 0x2, 0xc, 0xd, 0x7, 0x4, 0x2, 0x2, 
    0xd, 0xf, 0x5, 0x4, 0x3, 0x2, 0xe, 0xb, 0x3, 0x2, 0x2, 0x2, 0xf, 0x12, 
    0x3, 0x2, 0x2, 0x2, 0x10, 0xe, 0x3, 0x2, 0x2, 0x2, 0x10, 0x11, 0x3, 
    0x2, 0x2, 0x2, 0x11, 0x3, 0x3, 0x2, 0x2, 0x2, 0x12, 0x10, 0x3, 0x2, 
    0x2, 0x2, 0x13, 0x14, 0x8, 0x3, 0x1, 0x2, 0x14, 0x15, 0x5, 0x6, 0x4, 
    0x2, 0x15, 0x1b, 0x3, 0x2, 0x2, 0x2, 0x16, 0x17, 0xc, 0x4, 0x2, 0x2, 
    0x17, 0x18, 0x7, 0x5, 0x2, 0x2, 0x18, 0x1a, 0x5, 0x6, 0x4, 0x2, 0x19, 
    0x16, 0x3, 0x2, 0x2, 0x2, 0x1a, 0x1d, 0x3, 0x2, 0x2, 0x2, 0x1b, 0x19, 
    0x3, 0x2, 0x2, 0x2, 0x1b, 0x1c, 0x3, 0x2, 0x2, 0x2, 0x1c, 0x5, 0x3, 
    0x2, 0x2, 0x2, 0x1d, 0x1b, 0x3, 0x2, 0x2, 0x2, 0x1e, 0x24, 0x7, 0x3, 
    0x2, 0x2, 0x1f, 0x20, 0x7, 0x6, 0x2, 0x2, 0x20, 0x21, 0x5, 0x2, 0x2, 
    0x2, 0x21, 0x22, 0x7, 0x7, 0x2, 0x2, 0x22, 0x24, 0x3, 0x2, 0x2, 0x2, 
    0x23, 0x1e, 0x3, 0x2, 0x2, 0x2, 0x23, 0x1f, 0x3, 0x2, 0x2, 0x2, 0x24, 
    0x7, 0x3, 0x2, 0x2, 0x2, 0x5, 0x10, 0x1b, 0x23, 
  };

  atn::ATNDeserializer deserializer;
  _atn = deserializer.deserialize(_serializedATN);

  size_t count = _atn.getNumberOfDecisions();
  _decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    _decisionToDFA.emplace_back(_atn.getDecisionState(i), i);
  }
}

TroianiParser::Initializer TroianiParser::_init;
