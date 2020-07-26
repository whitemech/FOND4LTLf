#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    "ltlf2dfa @ git+https://github.com/whitemech/LTLf2DFA.git@develop#egg=ltlf2dfa"
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