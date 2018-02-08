# -*- coding: utf-8 -*-
#
# Copyright 2017 Evolent Health, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup, find_packages

import serverless


requires = []


def long_description():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='serverless',
    version=serverless.__version__,
    description=serverless.__doc__.strip(),
    long_description=long_description(),
    author=serverless.__author__,
    license=serverless.__licence__,    
    packages=find_packages(exclude=['tests']),
    install_requires=requires
)
