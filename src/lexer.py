import re

# token types
TOKEN_TYPES = {
    'SINGLE_LINE_COMMENT': r'\/\/[^\n]*',
    'MULTI_LINE_COMMENT': r'\/\*.*?\*\/|\/\*[^*]*\*+([^/*][^*]*\*+)*\/',
    'KEYWORD': r'(let|if|else|loop|function|public|private|class|import|export|try|catch|new|async)',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'"[^"]*"',
    'SINGLE_QUOTED_STRING': r"'[^']*'",
    'BOOL': r'(true|false)',
    'OPERATOR': r'(\+|-|\*|\/|==|!=|<|>|<=|>=|&|\||=)',
    'SEMICOLON': r';',
    'COLON': r':',
    'COMMA': r',',
    'DOT': r'\.',
    'OPEN_BRACE': r'{',
    'CLOSE_BRACE': r'}',
    'OPEN_PAREN': r'\(',
    'CLOSE_PAREN': r'\)',
    'WHITESPACE': r'\s+',
    'NEWLINE': r'\n',
}

# creating "combined" regex pattern..
TOKEN_PATTERN = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())
TOKEN_REGEX = re.compile(TOKEN_PATTERN)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.pos = 0

    def tokenize(self):
        try:
            with open(self.filename, 'r') as file:
                code = file.read()
                self.lex(code)
                return self.tokens
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

    def lex(self, code):
        while self.pos < len(code):
            match = TOKEN_REGEX.match(code, self.pos)
            if match:
                token_type = match.lastgroup
                token_value = match.group(token_type)
                if token_type not in ('SINGLE_LINE_COMMENT', 'MULTI_LINE_COMMENT'):
                    self.tokens.append(Token(token_type, token_value))
                self.pos = match.end()
            else:
                # raise error when char not in dictionary..
                raise ValueError(f"Invalid character: {code[self.pos]}")

# example:
if __name__ == '__main__':
    filename = '../diprex/test.dpr'
    lexer = Lexer(filename)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
