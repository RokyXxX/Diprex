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
        self.advance()  # Start with the first token
        self.ast = self.parse_statements()  # Parse statements at the top-level
        return self.ast

    def parse_statements(self):
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

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

        return {
            'type': 'if',
            'condition': condition,
            'body': body
        }

    def parse_variable_declaration(self):
        # TODO: Implement parsing for variable declarations
        # Example: let yomama as boolean, yomama = false
        pass

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

        return {
            'type': 'function',
            'name': name,
            'parameters': parameters,
            'body': body
        }

    def parse_class_definition(self):
        # TODO: Implement parsing for class definitions
        # Example: class Person { constructor(name as string, age as int) { ... } }
        pass

    def parse_import_statement(self):
        # TODO: Implement parsing for import statements
        # Example: import { xyz, pqr } from abc as 'idk';
        pass

    def parse_export_statement(self):
        # TODO: Implement parsing for export statements
        # Example: export default lollipop;
        pass

    def parse_try_catch_statement(self):
        # TODO: Implement parsing for try-catch statements
        # Example: try { ... } catch (err/error) { ... }
        pass

    def error(self, message):
        raise Exception(f"Parser Error: {message}")
