# -*- coding: utf-8 -*-

"""This module contains the implementations of a PDDL Literal."""


class Literal:
    """A class for the Literal."""

    def __init__(self, predicate, positiveness):
        """Initialize the Literal."""
        self.predicate = predicate
        self.positiveness = positiveness

    def is_positive(self):
        """Check if the Literal is positive."""
        return self.positiveness

    @classmethod
    def positive(cls, predicate):
        """Return a positive Literal."""
        return Literal(predicate, True)

    @classmethod
    def negative(cls, predicate):
        """Return a negative Literal."""
        return Literal(predicate, False)

    def get_vars(self):
        """Get variables."""
        return self.predicate.args

    def __repr__(self):
        """Get the representation."""
        return str(self)

    def __str__(self):
        """Represent the Literal as string."""
        if self.is_positive():
            return str(self.predicate)
        if not self.is_positive() and self.predicate.name == "=":
            lhs = str(self.predicate.args[0])
            rhs = str(self.predicate.args[1])
            return "(not (= {0} {1}))".format(lhs, rhs)
        if not self.is_positive():
            return "(not {})".format(str(self.predicate))
