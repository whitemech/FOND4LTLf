class Literal:

    def __init__(self, term, positiveness):
        self.term = term
        self.positiveness = positiveness

    def is_positive(self):
        return self.positiveness

    @classmethod
    def positive(cls, term):
        return Literal(term, True)

    @classmethod
    def negative(cls, term):
        return Literal(term, False)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.is_positive():
            return str(self.term)
        if not self.is_positive() and self.term.name == '=':
            lhs = str(self.term.args[0])
            rhs = str(self.term.args[1])
            return '{0} != {1}'.format(lhs, rhs)
        if not self.is_positive():
            return '(not {})'.format(str(self.term))