import re
import ast
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import coverage
        import pytest

        if self.pytest_args and len(self.pytest_args) > 0:
            self.test_args.extend(self.pytest_args.strip().split(' '))
            self.test_args.append('tests/')

        cov = coverage.Coverage()
        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.report()
        cov.html_report()
        print("Wrote coverage report to htmlcov directory")
        sys.exit(errno)


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('rho_zappa/__init__.py', 'rb') as f:
    __version__ = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='rho-zappa',
    version=__version__,
    description="Rho Zappa - template wrapper for Zappa",
    long_description=open('README.md', 'r').read(),
    maintainer="Rho AI",
    license="MIT",
    url="https://github.com/RhoAI/rho-zappa.git",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rho-zappa=rho_zappa.render_and_run:main'
        ]
    },
    install_requires=[
        'zappa==0.42.0',
        'Jinja2==2.9.6'
    ],
    extras_require={},
    tests_require=[
        'coverage==4.0a5',
        'mock==1.0.1',
        'tox==2.3.1'
    ],
    cmdclass={'test': PyTest}
)
