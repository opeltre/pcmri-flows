#!/usr/bin/env python
import os
from setuptools import setup

with open('./requirements.txt', 'r') as f:
    requirements = f.read().strip().split('\n')

setup(
    name    ='pcmri',
    version ='0.1',
    description ="PCMRI flows processing",
    author      ="Olivier Peltre",
    author_email='opeltre@gmail.com',
    url     ='https://github.com/opeltre/infusion',
    license ='MIT',
    install_requires=requirements,
    packages = ['pcmri'],
    exclude_package_data = {'': ['datasets']}
)
