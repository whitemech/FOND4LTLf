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
import ply.lex as lex


class PDDLLexer(object):

    reserved = {
        "define": "DEFINE_KEY",
        "domain": "DOMAIN_KEY",
        ":domain": "DOMAIN_PKEY",
        ":requirements": "REQUIREMENTS_KEY",
        ":constants": "CONSTANTS_KEY",
        ":strips": "STRIPS_KEY",
        ":adl": "ADL_KEY",
        ":non-deterministic": "ND_KEY",
        ":equality": "EQUALITY_KEY",
        ":typing": "TYPING_KEY",
        ":types": "TYPES_KEY",
        ":predicates": "PREDICATES_KEY",
        ":action": "ACTION_KEY",
        ":parameters": "PARAMETERS_KEY",
        ":precondition": "PRECONDITION_KEY",
        ":effect": "EFFECT_KEY",
        "and": "AND_KEY",
        "or": "OR_KEY",
        "not": "NOT_KEY",
        "imply": "IMPLY_KEY",
        "oneof": "ONEOF_KEY",
        "forall": "FORALL_KEY",
        "exists": "EXISTS_KEY",
        "when": "WHEN_KEY",
        "problem": "PROBLEM_KEY",
        ":objects": "OBJECTS_KEY",
        ":init": "INIT_KEY",
        ":goal": "GOAL_KEY",
    }

    # List of token names. This is always required
    tokens = ("NAME", "VARIABLE", "LPAREN", "RPAREN", "HYPHEN", "EQUALS") + tuple(
        reserved.values()
    )

    # Regular expression rules for simple tokens
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_HYPHEN = r"\-"
    t_EQUALS = r"="

    t_ignore = " \t"

    def t_KEYWORD(self, t):
        r":?[a-zA-z_][a-zA-Z_0-9\-]*"
        t.type = self.reserved.get(t.value, "NAME")
        return t

    def t_NAME(self, t):
        r"[0-9a-zA-z_][a-zA-Z_0-9\-]*"
        return t

    def t_VARIABLE(self, t):
        r"\?[a-zA-z_][a-zA-Z_0-9\-]*"
        return t

    def t_COMMENT(self, t):
        r";.*"
        pass

    # def t_PROBABILITY(self, t):
    #     r'[0-1]\.\d+'
    #     t.value = float(t.value)
    #     return t

    def t_newline(self, t):
        r"\n+"
        t.lineno += len(t.value)

    def t_error(self, t):
        print("Error: illegal character '{0}'".format(t.value[0]))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test the lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == "__main__":
    # Build the lexer and try it out
    m = PDDLLexer()
    m.build()  # Build the lexer
    m.test("(and (and) (oneof (ciao) (come) ))")  # Test it
