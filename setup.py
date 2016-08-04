from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import harpFinance

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='harpfin',
    version=harpFinance.__version__,
    url='https://github.com/harpribot/harpStocks/',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    author='Harshal Priyadarshi',
    tests_require=['pytest'],
    install_requires=['yahoo-finance',
                    ],
    cmdclass={'test': PyTest},
    author_email='harshal.priyadarshi@utexas.edu',
    description='Automated Real time Machine Learning based Stock Portfolio Manager',
    long_description=long_description,
    packages=['harpFinance'],
    include_package_data=True,
    platforms='any',
    test_suite='harpFinance.test.test_harpFinance',
    extras_require={
        'testing': ['pytest'],
    }
)
