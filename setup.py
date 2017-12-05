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
