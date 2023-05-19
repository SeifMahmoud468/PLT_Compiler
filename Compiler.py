import re

class Compiler:
    def __init__(self):
        self.tokens = []
        self.current_token = None
        self.index = 0
        self.output = []

    # takes an input string and splits it into a list of tokens using a regular expression
    def tokenize(self, input_string):
        self.tokens = re.findall(r'\w+|[^\s\w]', input_string)
        self.current_token = self.tokens[self.index]

    # it moves through the list of tokens, one at a time. It takes an expected token as an argument
    #if the current token matches, it advances to the next token in the list.
    # If there are no more tokens, it sets the current token to None.
    # If the current token does not match the expected token, it raises an exception.
    def consume(self, expected_token):
        if self.current_token == expected_token:
            self.index += 1
            if self.index < len(self.tokens):
                self.current_token = self.tokens[self.index]
            else:
                self.current_token = None
        else:
            raise Exception(f'Error: Expected {expected_token}, got {self.current_token}')

    #handles individual factors (numbers or variables)
    def factor(self):
        if re.match(r'\d+', self.current_token):
            value = int(self.current_token)
            self.output.append(f'LIT {value}')
            self.consume(self.current_token)
        elif re.match(r'\w+', self.current_token):
            value = self.current_token
            self.output.append(f'LIT {value}')
            self.consume(self.current_token)
            if self.current_token == '[':
                self.consume('[')
                self.expr()
                self.consume(']')
                self.output.append('ADD')
                self.output.append('LOAD')
            else:
                self.output.append('LOAD')
        else:
            raise Exception(f'Error: Invalid token {self.current_token}')

    #handles multiplication and division
    def term(self):
        self.factor()
        while self.current_token in ['*', '/']:
            op = self.current_token
            if op == '*':
                self.consume('*')
                self.factor()
                self.output.append('MUL')
            elif op == '/':
                self.consume('/')
                self.factor()
                self.output.append('DIV')

    # handles addition and subtraction
    def expr(self):
        if self.current_token == '-':
            op = '-'
            self.consume('-')
            if re.match(r'\d+', self.current_token):
                value = int(self.current_token)
                value *= -1
                value = str(value)
                value.replace('-', '')
                value = '-' + value
                value = int(value)
                value = str(value)
                value.replace('--', '')

                self.output.append(f'LIT {value}')
                self.consume(self.current_token)
            else:
                self.term()
                self.output.append('NEG')
        else:
            self.term()
        while self.current_token in ['+', '-']:
            op = self.current_token
            if op == '+':
                self.consume('+')
                self.term()
                self.output.append('ADD')
            elif op == '-':
                self.consume('-')
                self.term()
                self.output.append('SUB')

    # used to parse and compile variable assignments.
    # It starts by checking that the current token is a valid variable name
    # then reads the next token to see if it's an index into an array (indicated by the [ ] notation).
    # If it is, it compiles the expression inside the brackets and adds an ADD instruction to the output.
    # Then it compiles the expression on the right-hand side of the assignment, and adds a STORE instruction to the output.
    def assign(self):
        if re.match(r'\w+', self.current_token):
            value = self.current_token
            self.consume(self.current_token)
            if self.current_token == '[':
                self.consume('[')
                self.expr()
                self.consume(']')
                self.output.append('ADD')
            else:
                self.output.append(f'LIT {value}')
            self.consume('=')
            self.expr()
            self.output.append('STORE')
        else:
            raise Exception(f'Error: Invalid token {self.current_token}')

    # takes an input string, tokenizes it, and repeatedly calls assign() to compile each assignment in the input string.
    # The resulting output is a list of instructions, which are concatenated into a single string and printed.
    def compile(self, input_string):
        self.tokenize(input_string)
        while self.current_token is not None:
            self.assign()

def main():
    compiler = Compiler()
    input_string = 'A=B+3*C'
    compiler.compile(input_string)
    output_string = " ".join(compiler.output)
    print(output_string)

if __name__ == '__main__':
    main()

