<h1 align="center">
  FOND 4 LTL<sub>f</sub> - PLTL<sub>f</sub>
</h1>

<p align="center">
  <a href="https://pypi.org/project/FOND4LTLfPLTLf">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/ltlf2dfa" />
  </a>
  <a href="https://github.com/whitemech/FOND4LTLfPLTLf/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/badge/license-LGPLv3%2B-blue">
  </a>
</p>
<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/whitemech/FOND4LTLfPLTLf/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/whitemech/FOND4LTLfPLTLf/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/whitemech/FOND4LTLfPLTLf/workflows/docs/badge.svg">
  </a>
  <a href="https://codecov.io/gh/whitemech/FOND4LTLfPLTLf">
    <img src="https://codecov.io/gh/whitemech/FOND4LTLfPLTLf/branch/master/graph/badge.svg?token=KKWRAH29O7"/>
  </a>
</p>
<p align="center">
  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">
    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">
  </a>
  <a href="https://img.shields.io/badge/mypy-checked-blue">
    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">
  </a>
  <a href="https://img.shields.io/badge/isort-checked-yellow">
    <img alt="isort" src="https://img.shields.io/badge/isort-checked-yellow" />
  </a>
  <a href="https://img.shields.io/badge/code%20style-black-black">
    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
</p>
<p align="center">
<a href="https://doi.org/10.5281/zenodo.4876281"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4876281.svg" alt="DOI"></a>
</p>

FOND 4 LTL<sub>f</sub>/PLTL<sub>f</sub> is a tool that compiles Fully Observable Non-Deterministic (FOND) planning
problems with temporally extended goals, specified either in LTL<sub>f</sub> or in PLTL<sub>f</sub>, into classical FOND
planning problems.

It is also available online at [fond4ltlfpltlf.diag.uniroma1.it](https://fond4ltlf.herokuapp.com/).

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
git clone https://github.com/whitemech/FOND4LTLfPLTLf.git
cd fond4ltlfpltlf
pip install .
```

## How To Use

Use the command line interface:

```bash
fond4ltlfpltlf -d <path/to/domain.pddl> -p <path/to/problem.pddl> -g "formula"
```

You can also specify custom output paths for the new domain and the new problem using `--out-domain` or `-outd`
and `--out-problem` or `-outp`.

## Features

* Syntax and parsing support FOND Planning in PDDL
* Compilation of Deterministic Finite-state Automaton into PDDL

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py3.8`

To run only the code style checks: `tox -e flake8`

## License

FOND4LTL<sub>f</sub>/PLTL<sub>f</sub> is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).

Copyright 2019-2020 WhiteMech

## Author

[Francesco Fuggitti](https://francescofuggitti.github.io/)


