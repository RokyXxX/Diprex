import re

# token types
TOKEN_TYPES = {
    'KEYWORD': r'(let|if|else|loop|function|public|private|class|import|export|try|catch|new|async)',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'"[^"]*"',
    'BOOL': r'(true|false)',
    'OPERATOR': r'(\+|-|\*|\/|==|!=|<|>|<=|>=|&|\|)',
    'SEMICOLON': r';',
    'COLON': r':',
    'COMMA': r',',
    'DOT': r'.',
    'SINGLE_LINE_COMMENT': r'\/\/[^\n]*',
    'MULTI_LINE_COMMENT': r'\/\*.*?\*\/',
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
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0

    def lex(self):
        while self.pos < len(self.code):
            match = TOKEN_REGEX.match(self.code, self.pos)
            if match:
                token_type = match.lastgroup
                token_value = match.group(token_type)
                if token_type not in ('SINGLE_LINE_COMMENT', 'MULTI_LINE_COMMENT'):
                    self.tokens.append(Token(token_type, token_value))
                self.pos = match.end()
            else:
                # raise error when char not in dictionary..
                raise ValueError(f"Invalid character: {self.code[self.pos]}")

        return self.tokens

# example:
if __name__ == '__main__':
    code = 'let age as int; if age > 18 { printStatement.print("You are an adult."); }'
    lexer = Lexer(code)
    tokens = lexer.lex()
    for token in tokens:
        print(token)
# TODO: get code FROM source file "*.dpr"