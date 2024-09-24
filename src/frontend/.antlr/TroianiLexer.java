// Generated from /home/walterjtv/Escritorio/SIDE/Troiani/src/frontend/Troiani.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class TroianiLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PLUS=1, SUB=2, MUL=3, DIV=4, MOD=5, EXP=6, LE=7, LT=8, ID=9, INT_LIT=10, 
		FLOAT_LIT=11, CHAR_LIT=12;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"PLUS", "SUB", "MUL", "DIV", "MOD", "EXP", "LE", "LT", "ID", "DIGIT", 
			"INT_LIT", "FLOAT_LIT", "CHAR_LIT"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'+'", "'-'", "'*'", "'/'", "'%'", "'^'", "'<='", "'<'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "PLUS", "SUB", "MUL", "DIV", "MOD", "EXP", "LE", "LT", "ID", "INT_LIT", 
			"FLOAT_LIT", "CHAR_LIT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public TroianiLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Troiani.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\f<\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0001\u0000\u0001\u0000\u0001\u0001\u0001"+
		"\u0001\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0004\u0001"+
		"\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0001"+
		"\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0003\b0\b\b\u0001\t\u0001"+
		"\t\u0001\n\u0004\n5\b\n\u000b\n\f\n6\u0001\u000b\u0001\u000b\u0001\f\u0001"+
		"\f\u0000\u0000\r\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005"+
		"\u000b\u0006\r\u0007\u000f\b\u0011\t\u0013\u0000\u0015\n\u0017\u000b\u0019"+
		"\f\u0001\u0000\u0002\u0002\u0000AZaz\u0003\u0000AZ__az<\u0000\u0001\u0001"+
		"\u0000\u0000\u0000\u0000\u0003\u0001\u0000\u0000\u0000\u0000\u0005\u0001"+
		"\u0000\u0000\u0000\u0000\u0007\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000"+
		"\u0000\u0000\u0000\u000b\u0001\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000"+
		"\u0000\u0000\u000f\u0001\u0000\u0000\u0000\u0000\u0011\u0001\u0000\u0000"+
		"\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000\u0000"+
		"\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0001\u001b\u0001\u0000\u0000"+
		"\u0000\u0003\u001d\u0001\u0000\u0000\u0000\u0005\u001f\u0001\u0000\u0000"+
		"\u0000\u0007!\u0001\u0000\u0000\u0000\t#\u0001\u0000\u0000\u0000\u000b"+
		"%\u0001\u0000\u0000\u0000\r\'\u0001\u0000\u0000\u0000\u000f*\u0001\u0000"+
		"\u0000\u0000\u0011,\u0001\u0000\u0000\u0000\u00131\u0001\u0000\u0000\u0000"+
		"\u00154\u0001\u0000\u0000\u0000\u00178\u0001\u0000\u0000\u0000\u0019:"+
		"\u0001\u0000\u0000\u0000\u001b\u001c\u0005+\u0000\u0000\u001c\u0002\u0001"+
		"\u0000\u0000\u0000\u001d\u001e\u0005-\u0000\u0000\u001e\u0004\u0001\u0000"+
		"\u0000\u0000\u001f \u0005*\u0000\u0000 \u0006\u0001\u0000\u0000\u0000"+
		"!\"\u0005/\u0000\u0000\"\b\u0001\u0000\u0000\u0000#$\u0005%\u0000\u0000"+
		"$\n\u0001\u0000\u0000\u0000%&\u0005^\u0000\u0000&\f\u0001\u0000\u0000"+
		"\u0000\'(\u0005<\u0000\u0000()\u0005=\u0000\u0000)\u000e\u0001\u0000\u0000"+
		"\u0000*+\u0005<\u0000\u0000+\u0010\u0001\u0000\u0000\u0000,/\u0007\u0000"+
		"\u0000\u0000-0\u0007\u0001\u0000\u0000.0\u0003\u0013\t\u0000/-\u0001\u0000"+
		"\u0000\u0000/.\u0001\u0000\u0000\u00000\u0012\u0001\u0000\u0000\u0000"+
		"12\u000209\u00002\u0014\u0001\u0000\u0000\u000035\u0003\u0013\t\u0000"+
		"43\u0001\u0000\u0000\u000056\u0001\u0000\u0000\u000064\u0001\u0000\u0000"+
		"\u000067\u0001\u0000\u0000\u00007\u0016\u0001\u0000\u0000\u000089\u0001"+
		"\u0000\u0000\u00009\u0018\u0001\u0000\u0000\u0000:;\u0001\u0000\u0000"+
		"\u0000;\u001a\u0001\u0000\u0000\u0000\u0003\u0000/6\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}