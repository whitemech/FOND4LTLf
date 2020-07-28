# -*- coding: utf-8 -*-

"""This module contains the implementations of a PDDL Predicate."""


class Predicate:
    """A class for the PDDL Predicate."""

    def __init__(self, name, args=None):
        """Initialize the formula."""
        if args is None:
            args = []
        self._name = name
        self._args = args

    @property
    def name(self):
        """Get the name."""
        return self._name

    @property
    def args(self):
        """Get the args."""
        return self._args[:]

    @property
    def arity(self):
        """Get the arity."""
        return len(self._args)

    def __str__(self):
        """Get the string."""
        if self.name == "=":
            return "(= {0} {1})".format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return "({0})".format(self.name)
        else:
            return "({0} {1})".format(self.name, " ".join(map(str, self._args)))

    def __eq__(self, other):
        """Override equal operator."""
        return (
            isinstance(other, Predicate)
            and self.name == other.name
            and self.args == other.args
        )

    def __hash__(self):
        """Get the has of a Predicate."""
        return id(self)
