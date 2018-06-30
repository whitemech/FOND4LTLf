class FormulaAnd:

    def __init__(self, formulaList):
        self.formulaList = formulaList

    def __str__(self):
        return self.formulaList

    def __iter__(self):
        return iter(self.formulaList)

class FormulaOr:

    def __init__(self, formulaList):
        self.formulaList = formulaList

    def __str__(self):
        return self.formulaList

    def __iter__(self):
        return iter(self.formulaList)

class FormulaNot:

    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return '(not' +self.formula +')'

    def __iter__(self):
        return '(not' + str(self.formula) +')'           

class FormulaImply:

    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __str__(self):
        return self.formula1 + self.formula2

    def __iter__(self):
        raise NotImplementedError
