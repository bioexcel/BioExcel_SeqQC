#! /usr/bin/env python

'''
Setup script for bioexcel_seqqc.
'''

from distutils.command.install import INSTALL_SCHEMES
from setuptools import setup

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='bioexcel_seqqc',
    version='0.2.0',
    description=('Sequence Quality Control python package'),
    author='Darren White',
    author_email='d.white@epcc.ed.ac.uk',
    scripts=['bin/bioexcel_seqqc'],
    packages=['bioexcel_seqqc'],
    package_dir={'bioexcel_seqqc': 'bioexcel_seqqc'},
    install_requires=['pyyaml'],
    data_files=[('bioexcel_seqqc', ['data/checkQC.yml'])],
)
