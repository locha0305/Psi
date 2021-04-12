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
            if char != ' ':
                word += char

        InExprLexerPointer.advance()

    Tokenized.append({'number': word})

    return Tokenized


def LineNotComment(line):
    line.split(' ')
    for char in line:
        if char == '':
            pass
        elif char == '#':
            return False

    return True


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


        line = code[LineLexerPointer.pos]  # set line

        while InlineLexerPointer.pos < len(line):

            char = line[InlineLexerPointer.pos]  # set char

            if char in Grammer.Identifier.identifier and not(char == '#'):  # when certain argument and not comment

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

                        if name_type == '':
                            name_type = '__anon__'

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '}':
                                expr += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '}'")

                        Tokenized.append({'type': 'var', 'name_type': name_type, 'expr': ExprLexer(expr)})

                    elif word == 'recv':  # variable statement

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

                        if name_type == '':
                            raise SyntaxError("Anonymous statement is not available for 'recv'")

                        InlineJumpPointer.reset()

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '}':
                                expr += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '}'")

                        Tokenized.append({'type': 'recv', 'name_type': name_type, 'expr': ExprLexer(expr)})

                    elif word == 'class':  # base class declare

                        word = ''
                        name_type = ''
                        attributes = ''

                        InlineJumpPointer.reset()
                        InlineLexerPointer.advance()

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '{':
                                if not(line[InlineLexerPointer.pos + InlineJumpPointer.jump] == ' '):
                                    name_type += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '{'")

                        if line[-1] == '}':  # class declare in one line
                            InlineJumpPointer.reset()

                            while InlineLexerPointer.pos + InlineJumpPointer.jump < len(line) - 1:
                                attributes += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                            Tokenized.append({'type': 'class', 'name_type': name_type, 'attributes': lex(attributes)})

                        else:

                            InlineJumpPointer.reset()

                            attributes = '\n'
                            LineJumpPointer = JumpPointer()

                            try:
                                while code[LineLexerPointer.pos + LineJumpPointer.jump - 1] != '}':  # just to check for '}'
                                    if LineNotComment(code[LineLexerPointer.pos + LineJumpPointer.jump]):
                                        attributes += code[LineLexerPointer.pos + LineJumpPointer.jump] + '\n'
                                    LineJumpPointer.advance()
                                LineLexerPointer.pos += LineJumpPointer.jump - 1  # because jump once at end of line
                                InlineLexerPointer.reset()
                                Tokenized.append({'type': 'class', 'name_type': name_type, 'attributes': lex(attributes)})
                                break
                            except IndexError:
                                raise SyntaxError("Missing '}'")

                    elif word == 'meth':  # method declare

                        word = ''
                        name_type = ''
                        attributes = ''
                        arguments = ''

                        InlineJumpPointer.reset()
                        InlineLexerPointer.advance()

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != ':' and line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '{':
                                if not (line[InlineLexerPointer.pos + InlineJumpPointer.jump] == ' '):
                                    name_type += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()

                        except IndexError:  # when no '{'
                            raise SyntaxError("Missing '{' or ':'")

                        if line[InlineLexerPointer.pos + InlineJumpPointer.jump] == ':':  # if decider
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                            InlineJumpPointer.reset()

                            decider = ''

                            try:
                                while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '(':
                                    if not (line[InlineLexerPointer.pos + InlineJumpPointer.jump] == ' '):
                                        decider += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                    InlineJumpPointer.advance()
                                InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                                if decider != 'give':
                                    raise SyntaxError("Invalid decider '{}'".format(decider))
                                else:
                                    InlineJumpPointer.reset()
                                    try:
                                        while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != ')':
                                            arguments += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                            InlineJumpPointer.advance()
                                        InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                                    except IndexError:
                                        raise SyntaxError("Missing ')'")

                            except IndexError:
                                raise SyntaxError("Missing '('")

                        if line[-1] == '}':
                            InlineJumpPointer.reset()

                            while InlineLexerPointer.pos + InlineJumpPointer.jump < len(line) - 1:
                                attributes += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1
                            Tokenized.append(
                                {'type': 'meth', 'name_type': name_type, 'give': lex('\n'.join(arguments.split(';'))), 'attributes': lex(attributes)})

                        else:

                            InlineJumpPointer.reset()

                            attributes = '\n'
                            LineJumpPointer = JumpPointer()

                            try:
                                while code[LineLexerPointer.pos + LineJumpPointer.jump - 1] != '}':  # just to check for '}'
                                    if LineNotComment(code[LineLexerPointer.pos + LineJumpPointer.jump]):
                                        attributes += code[LineLexerPointer.pos + LineJumpPointer.jump] + '\n'
                                    LineJumpPointer.advance()
                                LineLexerPointer.pos += LineJumpPointer.jump - 1  # because jump once at end of line
                                InlineLexerPointer.reset()
                                Tokenized.append(
                                    {'type': 'meth', 'name_type': name_type, 'give': lex(arguments), 'attributes': lex(attributes)})
                                break
                            except IndexError:
                                raise SyntaxError("Missing '}'")

                    elif word == 'return':
                        InlineJumpPointer.reset()
                        InlineJumpPointer.advance()
                        expr = ''

                        try:
                            while line[InlineLexerPointer.pos + InlineJumpPointer.jump] != '}':
                                expr += line[InlineLexerPointer.pos + InlineJumpPointer.jump]
                                InlineJumpPointer.advance()
                            InlineLexerPointer.pos += InlineJumpPointer.jump + 1

                        except IndexError:
                            raise SyntaxError("Missing '}'")

                        Tokenized.append({'type': 'return', 'expr': ExprLexer(expr)})

                else:  # variable assignment/class declare

                    name_type = word
                    if name_type == '':  # just empty
                        pass
                    else:
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
                            Tokenized.append({'type': 'var_assign', 'name_type': name_type, 'expr': ExprLexer(expr)})

                        else:
                            raise SyntaxError('{}'.format(name_type))
            elif char == '#':
                break
            else:
                word += char

            InlineLexerPointer.advance()

        LineLexerPointer.advance()

    return Tokenized


with open('test', 'r', encoding='UTF-8') as file:
    Code = ''.join(file.readlines())

print(lex(Code))





