# -*- coding: utf-8 -*-

"""This module contains the implementations of an automaton Symbol."""


class Symbol:
    """A class for the Symbol of a DFA."""

    def __init__(self, name, objects_list=None):
        """Initialize the Symbol."""
        if objects_list is None:
            objects_list = []
        self.name = name
        self.objects = objects_list

    def __str__(self):
        """Get the string."""
        return "{0} - {1}".format(self.name, ",".join(self.objects))

    def __hash__(self):
        """Get the hash."""
        if self.objects:
            return hash(self.name + str("_".join(self.objects)))
        else:
            return hash(self.name)

    def __eq__(self, other):
        """Override the equal operator."""
        if self.name == other.name and self.objects == other.objects:
            return True
        else:
            return False
