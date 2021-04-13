class VarStatement:
    def __init__(self, Super, name, value):
        self.Super = Super
        self.name = name
        self.value = value

    def __repr__(self):
        return str((self.Super, self.name, self.value))


class RecvStatement:
    def __init__(self, Super, name, value):
        self.Super = Super
        self.name = name
        self.value = value

    def __repr__(self):
        return str((self.Super, self.name, self.value))


class ClassStatement:
    def __init__(self, Super, name, attributes):
        self.Super = Super
        self.name = name
        self.attributes = attributes

    def __repr__(self):
        return str((self.Super, self.name, self.attributes))


class MethodStatement:
    def __init__(self, Super, name, give, attributes):
        self.Super = Super
        self.name = name
        self.give = give
        self.attributes = attributes

    def __repr__(self):
        return str((self.Super, self.name, self.give, self.attributes))


class ReturnStatement:
    def __init__(self, Super, expr):
        self.Super = Super
        self.expr = expr

    def __repr__(self):
        return str((self.Super, self.expr))