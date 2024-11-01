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

    def __eq__(self, other):
        """Check the equality between two Literals."""
        return (
            isinstance(other, Literal)
            and self.predicate == other.predicate
            and self.positiveness == other.positiveness
        )

    def __hash__(self):
        """Get the has of a Literal."""
        return id(self)
