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
        return self.name == other.name and self.objects == other.objects
