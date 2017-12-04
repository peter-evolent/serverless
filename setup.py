from setuptools import setup, find_packages

import os
import re


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


requires = []


def get_version():
    init = open(os.path.join(ROOT, 'serverless', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='serverless',
    description='serverless sdk',
    version=get_version(),
    packages=find_packages(exclude=['tests']),
    install_requires=requires,
    author='Peter Hwang',
    license='Apache License 2.0'
)
