#! /usr/bin/env python

from setuptools import setup

setup(
    name='SeqQC',
    version='0.1.0',
    description=('Sequence Quality Control python module'),
    author='Darren White',
    author_email='d.white@epcc.ed.ac.uk',
    scripts=['bin/SeqQC'],
    packages=['seq_qc'],
    package_dir={'seq_qc': 'seq_qc'},
    install_requires=[],
)