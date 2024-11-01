#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of FOND4LTLf.
#
# FOND4LTLf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FOND4LTLf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FOND4LTLf.  If not, see <https://www.gnu.org/licenses/>.
#

"""This module contains the implementations of a PDDL Term."""


class Term:
    """A class for the PDDL Term."""

    def __init__(self, **kwargs):
        """Initialize the Term."""
        self._name = kwargs.get("name", None)
        self._type = kwargs.get("type", None)
        self._value = kwargs.get("value", None)

    @property
    def name(self):
        """Get the name."""
        return self._name

    @property
    def type(self):
        """Get the type."""
        return self._type

    @property
    def value(self):
        """Get the value."""
        return self._value

    def is_variable(self):
        """Check if it is a variable."""
        return self._name is not None

    def is_typed(self):
        """Check if it is typed."""
        return self._type is not None

    def is_constant(self):
        """Check if it is a constant."""
        return self._value is not None

    @classmethod
    def variable(cls, name, type=None):
        """Return a variable Term."""
        return Term(name=name, type=type)

    @classmethod
    def constant(cls, value, type=None):
        """Return a constant Term."""
        return Term(value=value, type=type)

    def __str__(self):
        """Get the string."""
        if self.is_variable() and self.is_typed():
            return "{0} - {1}".format(self._name, self._type)
        if self.is_variable():
            return "{0}".format(self._name)
        if self.is_constant() and self.is_typed():
            return "{0} - {1}".format(self._value, self._type)
        if self.is_constant():
            return "{0}".format(self._value)

    def __eq__(self, other):
        """Check equality between two Terms."""
        if self.is_variable():
            return (
                isinstance(other, Term)
                and self._name == other._name
                and self._type == other._type
            )
        else:
            assert self.is_constant()
            return (
                isinstance(other, Term)
                and self._value == other._value
                and self._type == other._type
            )

    def __hash__(self):
        """Get the hash of a Term."""
        return id(self)
