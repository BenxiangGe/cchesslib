# -*- coding: utf-8 -*-
'''
Copyright (C) 2014  walker li <walker8088@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

""" Vispy setup script.

Steps to do a new release:

Preparations:
  * Test on Windows, Linux, Mac
  * Make release notes
  * Update API documentation and other docs that need updating.

Test installation:
  * clear the build and dist dir (if they exist)
  * python setup.py register -r http://testpypi.python.org/pypi
  * python setup.py sdist upload -r http://testpypi.python.org/pypi
  * pip install -i http://testpypi.python.org/pypi

Define the version:
  * update __version__ in __init__.py
  * Tag the tip changeset as version x.x

Generate and upload package (preferably on Windows)
  * python setup.py register
  * python setup.py sdist upload
  * python setup.py bdist_wininst upload

"""

import os
from os import path as op
from warnings import warn

try:
    # use setuptools namespace, allows for "develop"
    import setuptools  # noqa, analysis:ignore
except ImportError:
    warn("unable to load setuptools. 'setup.py develop' will not work")
    pass  # it's not essential for installation
from distutils.core import setup

name = 'cchess'
description = 'ChineseChess in Python'

# Get version and docstring
__version__ = None
__doc__ = ''
docStatus = 0  # Not started, in progress, done
initFile = os.path.join(os.path.dirname(__file__), 'vispy', '__init__.py')
for line in open(initFile).readlines():
    if (line.startswith('version_info') or line.startswith('__version__')):
        exec(line.strip())
    elif line.startswith('"""'):
        if docStatus == 0:
            docStatus = 1
            line = line.lstrip('"')
        elif docStatus == 1:
            docStatus = 2
    if docStatus == 1:
        __doc__ += line


def package_tree(pkgroot):
    path = os.path.dirname(__file__)
    subdirs = [os.path.relpath(i[0], path).replace(os.path.sep, '.')
               for i in os.walk(os.path.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


setup(
    name=name,
    version=__version__,
    author='Walker Li',
    author_email='walker8088@gmail.com',
    license='GPL-3.0',
    url='https://github.com/walker8088/cchess',
    download_url='https://pypi.python.org/pypi/cchess',
    keywords="ChineseChess",
    description=description,
    long_description=__doc__,
    platforms='any',
    provides=['walker'],
    install_requires=[''],
    extras_require={
        
    },
    packages=package_tree('cchess'),
    package_dir={
        'cchess': 'cchess'},
    package_data={
                  },
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: GPL-3.0',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
