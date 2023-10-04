class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.current_index = 0
        self.ast = None

    def advance(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.current_index += 1

    def parse(self):
        self.advance()
        self.ast = self.parse_statements()
        return self.ast

    def parse_statements(self):
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            self.eat('SEMICOLON')
        return statements
    
    def eat(self, expected_type):
        if self.current_token.type == expected_type:
            self.advance()
        else:
            self.error(f"Expected '{expected_type}' but found '{self.current_token.type}'")

    def parse_statement(self):
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'let':
            return self.parse_variable_declaration()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            return self.parse_if_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'function':
            return self.parse_function_definition()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'class':
            return self.parse_class_definition()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'import':
            return self.parse_import_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'export':
            return self.parse_export_statement()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'try':
            return self.parse_try_catch_statement()
        elif self.current_token.type == 'SINGLE_LINE_COMMENT' or self.current_token.type == 'MULTI_LINE_COMMENT':
            self.advance()  # comment skiping go brrrrrr
            return None
        else:
            self.error(f"Unexpected token: {self.current_token.type}")

    def parse_if_statement(self):
        condition = None
        body = None

        # expect 'if' keyword
        self.expect('KEYWORD', 'if')
        self.expect('OPEN_PAREN', '(')

        condition = self.parse_expression()

        self.expect('CLOSE_PAREN', ')')
        self.expect('OPEN_BRACE', '{')

        body = self.parse_statements()

        self.expect('CLOSE_BRACE', '}')
        self.eat('SEMICOLON')

        return {
            'type': 'if',
            'condition': condition,
            'body': body
        }

    def parse_variable_declaration(self):
        name = None
        data_type = None

        # expect 'let' keyword
        self.expect('KEYWORD', 'let')

        name = self.expect('IDENTIFIER')

        # expect 'as' keyword
        self.expect('KEYWORD', 'as')

        data_type = self.expect('IDENTIFIER')

        # checking for optional init.
        initialization = None
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '=':
            self.advance()  # Move past '='
            initialization = self.parse_expression()

        # expect semicolon to end the declaration
        self.eat('SEMICOLON')

        return {
            'type': 'variable_declaration',
            'name': name,
            'data_type': data_type,
            'initialization': initialization
        }

    def parse_function_definition(self):
        name = None
        parameters = []
        body = None

        # expect 'function' keyword
        self.expect('KEYWORD', 'function')

        name = self.expect('IDENTIFIER')

        self.expect('OPEN_PAREN', '(')

        while self.current_token.type != 'CLOSE_PAREN':
            param_name = self.expect('IDENTIFIER')
            self.expect('AS')
            param_type = self.expect('IDENTIFIER')
            parameters.append({'name': param_name, 'type': param_type})
            if self.current_token.type == 'COMMA':
                self.advance()

        self.expect('CLOSE_PAREN', ')')
        self.expect('OPEN_BRACE', '{')

        body = self.parse_statements()

        self.expect('CLOSE_BRACE', '}')
        self.eat('SEMICOLON')

        return {
            'type': 'function',
            'name': name,
            'parameters': parameters,
            'body': body
        }

    def parse_class_definition(self):
        name = None
        properties = []

        # expect 'class' keyword
        self.expect('KEYWORD', 'class')

        name = self.expect('IDENTIFIER')

        self.expect('OPEN_BRACE', '{')

        while self.current_token.type != 'CLOSE_BRACE':
            prop_name = self.expect('IDENTIFIER')
            self.expect('AS')
            prop_type = self.expect('IDENTIFIER')
            properties.append({'name': prop_name, 'type': prop_type})
            if self.current_token.type == 'COMMA':
                self.advance()

        self.expect('CLOSE_BRACE', '}')
        self.eat('SEMICOLON')

        return {
            'type': 'class',
            'name': name,
            'properties': properties
        }

    def parse_import_statement(self):
        # expect 'import' keyword
        self.expect('KEYWORD', 'import')

        # parse imports (for simple life, let's think of importing everything)
        self.expect('OPEN_BRACE', '{')
        self.expect('IDENTIFIER')
        while self.current_token.type == 'COMMA':
            self.advance()
            self.expect('IDENTIFIER')
            self.expect('CLOSE_BRACE', '}')

        # expect 'from' keyword
        self.expect('KEYWORD', 'from')

        module_name = self.expect('IDENTIFIER')

        # expect 'as' keyword and alias
        self.expect('KEYWORD', 'as')
        alias = self.expect('STRING')['value']
        self.eat('SEMICOLON')

        return {
            'type': 'import',
            'module_name': module_name,
            'alias': alias
        }

    def parse_export_statement(self):
        # expect 'export' keyword
        self.expect('KEYWORD', 'export')

        # expect 'default' keyword and exported thing
        self.expect('KEYWORD', 'default')
        exported_item = self.expect('IDENTIFIER')
        self.eat('SEMICOLON')

        return {
            'type': 'export',
            'exported_item': exported_item
        }
        pass

    def parse_try_catch_statement(self):
        try_block = None
        catch_block = None

        # expect 'try' keyword
        self.expect('KEYWORD', 'try')
        self.expect('OPEN_BRACE', '{')

        try_block = self.parse_statements()

        self.expect('CLOSE_BRACE', '}')

        # expect 'catch' keyword
        self.expect('KEYWORD', 'catch')

        self.expect('OPEN_PAREN', '(')
        exception_variable = self.expect('IDENTIFIER')
        self.expect('CLOSE_PAREN', ')')
        self.expect('OPEN_BRACE', '{')

        catch_block = self.parse_statements()

        self.expect('CLOSE_BRACE', '}')
        self.eat('SEMICOLON')

        return {
            'type': 'try_catch',
            'try_block': try_block,
            'exception_variable': exception_variable,
            'catch_block': catch_block
        }

    def error(self, message):
        raise Exception(f"DipRex [ERROR]: Error while parsing: {message}")
