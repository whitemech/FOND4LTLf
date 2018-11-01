class Literal:

    def __init__(self, predicate, positiveness):
        self.predicate = predicate
        self.positiveness = positiveness

    def is_positive(self):
        return self.positiveness

    @classmethod
    def positive(cls, predicate):
        return Literal(predicate, True)

    @classmethod
    def negative(cls, predicate):
        return Literal(predicate, False)

    def get_vars(self):
        return self.predicate.args

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.is_positive():
            return str(self.predicate)
        if not self.is_positive() and self.predicate.name == '=':
            lhs = str(self.predicate.args[0])
            rhs = str(self.predicate.args[1])
            return '(not (= {0} {1}))'.format(lhs, rhs)
        if not self.is_positive():
            return '(not {})'.format(str(self.predicate))