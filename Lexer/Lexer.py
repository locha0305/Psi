import Grammer.Identifier
import Grammer.Arguments


class LexerPointer:
    def __init__(self):
        self.pos = 0

    def reset(self):
        self.pos = 0

    def advance(self):
        self.pos += 1


class JumpPointer:
    def __init__(self):
        self.jump = 1

    def reset(self):
        self.jump = 0

    def advance(self):
        self.jump += 1


def ExprLexer(expr):
    InExprLexerPointer = LexerPointer()
    word = ''
    Tokenized = []

    while InExprLexerPointer.pos < len(expr):
        char = expr[InExprLexerPointer.pos]
        if char in Grammer.Identifier.operator:
            Tokenized.append({'number': word})
            Tokenized.append({'operator': char})
            word = ''
        else:
            word += char

        InExprLexerPointer.advance()

    Tokenized.append({'number': word})

    return Tokenized



def lex(code):
    Tokenized = []  # lex result
    code = code.split('\n')  # split lines

    LineLexerPointer = LexerPointer()  # new line LexerPointer object
    InlineLexerPointer = LexerPointer()  # new inline LexerPointer object
    InlineJumpPointer = JumpPointer()  # new inline JumpPointer object

    word = ''  # word

    while LineLexerPointer.pos < len(code):  # each line

        InlineLexerPointer.reset()  # reset pointer
        InlineJumpPointer.reset()  # reset pointer

        word = ''  # reset word

        LineTokenizedResult = []  # each tokenized result for line

        line = code[LineLexerPointer.pos]  # set line

        while InlineLexerPointer.pos < len(line):

            char = line[InlineLexerPointer.pos]  # set char

            if char in Grammer.Identifier.identifier:  # when certain argument

                if word in Grammer.Arguments.arguments:

                    if word == 'var':  # variable statement

                        word = ''  # reset word
                        name_type = ''  # <name_type>
                        expr = ''  # <expr>

                        InlineJumpPointer.reset()  # reset jump
                        InlineLexerPointer.advance()  # to avoid adding ' '

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '{':
                                if not(line[InlineLexerPointer.pos + InlineJumpPointer.jump] == ' '):
                                    name_type += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1  # to avoid adding '{'
                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '{'")

                        InlineJumpPointer.reset()

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '}':
                                expr += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump
                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '}'")

                        LineTokenizedResult.append({'type': 'var', 'name_type': name_type, 'expr': ExprLexer(expr)})

                else:  # variable assignment/class declare

                    name_type = word
                    next_name_type = ''
                    word = ''  # reset word

                    InlineJumpPointer.reset()  # reset jump
                    InlineLexerPointer.advance()  # to avoid adding ' '

                    try:
                        while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != ' ':
                            next_name_type += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                            InlineJumpPointer.advance()
                        InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                        InlineJumpPointer.reset()
                    except IndexError:
                        raise SyntaxError('{}'.format(name_type))

                    if next_name_type == '=':  # variable assignment

                        InlineJumpPointer.reset()

                        expr = ''  # <expr>

                        while InlineLexerPointer.pos + InlineJumpPointer.jump < len(line):
                            expr += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                            InlineJumpPointer.advance()

                        InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                        InlineJumpPointer.reset()
                        LineTokenizedResult.append({'type': 'var_assign', 'name_type': name_type, 'expr': ExprLexer(expr)})

                    else:
                        pass

            else:
                word += char

            InlineLexerPointer.advance()

        Tokenized.append(LineTokenizedResult)

        LineLexerPointer.advance()

    return Tokenized


print(lex('var some_kind_of_a_random_number{12 + 3/2 + 3}\nvar b{1.2 * 3/1.5**2||2}\na = 12+3/2'))



