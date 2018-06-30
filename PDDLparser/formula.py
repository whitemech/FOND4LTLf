class FormulaAnd:

    def __init__(self, formulaList):
        self.formulaList = formulaList

    def __str__(self):
        return self.formulaList

    def __iter__(self):
        return iter(self.formulaList)