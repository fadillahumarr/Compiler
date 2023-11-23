# Token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
STRING = 'STRING'
EOF = 'EOF'

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, message="Karakter tidak valid"):
        raise Exception(f'{message} pada posisi {self.pos}')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)

    def string(self):
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip the closing quote
        else:
            self.error("String tidak ditutup dengan benar.")
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '"':
                return Token(STRING, self.string())

            self.error()

        return Token(EOF, None)

# Token types
# (tidak perlu diubah)

# Token class
# (tidak perlu diubah)

# Lexer
# (tidak perlu diubah)

# Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Sintaks tidak valid"):
        raise Exception(f'{message} pada posisi {self.lexer.pos}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return str(token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == STRING:
            self.eat(STRING)
            return f'"{token.value}"'

    def term(self):
        result = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result = f'{result} * {self.factor()}'
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = f'{result} / {self.factor()}'
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = f'{result} + {self.term()}'
            elif token.type == MINUS:
                self.eat(MINUS)
                result = f'{result} - {self.term()}'
        return result

# Main
def main():
    try:
        file_name = input('Masukkan nama file teks: ')
        output_file_name = input('Masukkan nama file Python output: ')

        with open(file_name, 'r') as file, open(output_file_name, 'w') as output_file:
            output_file.write("# Hasil kompilasi dari ekspresi matematika\n")
            output_file.write("if __name__ == '__main__':\n")
            output_file.write("    result = []\n")

            for line in file:
                lexer = Lexer(line)
                parser = Parser(lexer)
                compiled_code = parser.expr()
                output_file.write(f"    result.append({compiled_code})\n")

            output_file.write("    print(result)\n")

        print(f'File Python output telah dibuat: {output_file_name}')

    except FileNotFoundError:
        print(f'File dengan nama {file_name} tidak ditemukan.')
    except Exception as e:
        print(f'Terjadi kesalahan: {e}')

if __name__ == '__main__':
    main()
