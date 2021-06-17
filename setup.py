#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of fond4ltlfpltlf.
#
# fond4ltlfpltlf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fond4ltlfpltlf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fond4ltlfpltlf.  If not, see <https://www.gnu.org/licenses/>.
#

"""The setup script."""
import os

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'fond4ltlfpltlf', '__version__.py'), 'r') as f:
    exec(f.read(), about)


install_requires = [
    "click",
    "ply",
    "ltlf2dfa"
]

setup(
    name=about['__title__'],
    description=about['__description__'],
    version=about['__version__'],
    author=about['__author__'],
    url=about['__url__'],
    author_email=about["__author_email__"],
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    install_requires=install_requires,
    license=about["__license__"],
    keywords='fond4ltlfpltlf',
    packages=find_packages(include=['fond4ltlfpltlf*']),
    entry_points={
        'console_scripts': ["fond4ltlfpltlf=fond4ltlfpltlf.__main__:main"],
    },
    test_suite='tests',
    zip_safe=False,
)