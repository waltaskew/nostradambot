#!/usr/bin/env python
"""setup.py"""

import setuptools

setuptools.setup(
    name='nostradambot',
    version='0.0.0',
    description='HipChat Bot for Nostradamus',
    author='Walt Askew',
    author_email='waltaskew@gmail.com',
    url='http://github.com/waltaskew/nostradambot',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=open('requirements.txt').readlines(),
    package_data={'': ['*.html']},
    include_package_data=True,
)
