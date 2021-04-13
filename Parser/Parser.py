import ParseTokens
import Lexer.Lexer


def parse(Super, tokens):
    Parsed = []

    for token in tokens:
        if token['type'] == 'var':
            Parsed.append(ParseTokens.VarStatement(Super, token['name_type'], token['expr']))
        elif token['type'] == 'recv':
            Parsed.append(ParseTokens.RecvStatement(Super, token['name_type'], token['expr']))
        elif token['type'] == 'class':
            Parsed.append(ParseTokens.ClassStatement(Super, token['name_type'], parse(token['name_type'], token['attributes'])))
        elif token['type'] == 'meth':
            Parsed.append(ParseTokens.MethodStatement(Super, token['name_type'], parse(token['name_type'], token['give']), parse(token['name_type'], token['attributes'])))
        elif token['type'] == 'return':
            Parsed.append(ParseTokens.ReturnStatement(Super, token['expr']))
    return Parsed


with open('test', 'r', encoding='UTF-8') as file:
    Code = ''.join(file.readlines())
print(parse('_global_', Lexer.Lexer.lex(Code)))
