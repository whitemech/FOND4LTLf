# FOND 4 LTL<sub>f</sub>/PLTL<sub>f</sub>
[![](https://img.shields.io/pypi/pyversions/fond4ltlfpltlf.svg)](https://pypi.python.org/pypi/fond4ltlfpltlf)
[![FOND4LTLfPLTLf CI pipeline](
  https://github.com/whitemech/FOND4LTLfPLTLf/workflows/FOND4LTLfPLTLf%20CI%20pipeline./badge.svg)](
  https://github.com/whitemech/FOND4LTLfPLTLf/actions?query=workflow%3A%22FOND4LTLfPLTLf+CI+pipeline.%22)
[![](https://img.shields.io/badge/status-development-orange.svg)](https://img.shields.io/badge/status-development-orange.svg)
[![codecov](https://codecov.io/gh/whitemech/FOND4LTLfPLTLf/branch/master/graph/badge.svg)](https://codecov.io/gh/whitemech/FOND4LTLfPLTLf)
[![](https://img.shields.io/badge/flake8-checked-blueviolet)](https://img.shields.io/badge/flake8-checked-blueviolet)
[![](https://img.shields.io/badge/mypy-checked-blue)](https://img.shields.io/badge/mypy-checked-blue)
[![](https://img.shields.io/badge/license-LGPLv3%2B-blue)](https://img.shields.io/badge/license-LGPLv3%2B-blue)

FOND 4 LTL<sub>f</sub>/PLTL<sub>f</sub> is a tool that compiles Fully Observable Non-Deterministic (FOND) planning 
problems with temporally extended goals, specified either in LTL<sub>f</sub> or in PLTL<sub>f</sub>, into classical 
FOND planning problems.

It is also available online at [fond4ltlfpltlf.diag.uniroma1.it](http://fond4ltlfpltlf.diag.uniroma1.it).

## Prerequisites

This tool is based on the following libraries:

- [ltlf2dfa 1.0.1](https://pypi.org/project/ltlf2dfa/)
- [ply](https://pypi.org/project/ply/)
- [click](https://pypi.org/project/click/)

They are automatically added while installing FOND4LTL<sub>f</sub>/PLTL<sub>f</sub>.

## Install

- Intall from source (`master` branch):
```
pip install git+https://github.com/whitemech/FOND4LTLfPLTLf.git
```

- or, clone the repository and install:
```
git clone htts://github.com/whitemech/FOND4LTLfPLTLf.git
cd fond4ltlfpltlf
pip install .
```
## How To Use
Use the command line interface:
```bash
fond4ltlfpltlf -d <path/to/domain.pddl> -p <path/to/problem.pddl> -g "formula"
```
You can also specify custom output paths for the new domain and the new problem 
using `--out-domain` or `-outd` and `--out-problem` or `-outp`.

## Features

* Syntax and parsing support FOND Planning in PDDL
* Compilation of Deterministic Finite-state Automaton into PDDL

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py37`

To run only the code style checks: `tox -e flake8`

## License

FOND4LTL<sub>f</sub>/PLTL<sub>f</sub> is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).

Copyright 2019-2020 WhiteMech

## Author

[Francesco Fuggitti](https://francescofuggitti.github.io/)


