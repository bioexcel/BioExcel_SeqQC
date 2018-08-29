#! /usr/bin/env python

from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='SeqQC_BioExcel',
    version='0.2.0',
    description=('Sequence Quality Control python package'),
    author='Darren White',
    author_email='d.white@epcc.ed.ac.uk',
    scripts=['bin/seqqc_bioexcel'],
    packages=['seqqc_bioexcel'],
    package_dir={'seqqc_bioexcel': 'seqqc_bioexcel'},
    install_requires=[],
    data_files=[('seqqc_bioexcel', ['data/checkQC.yml'])],
)
