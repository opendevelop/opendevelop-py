#!/usr/bin/env python

from distutils.core import setup
import os

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

with open('./requirements.txt') as requirements_txt:
    requirements = [line for line in requirements_txt]

setup(name='OpenDevelop',
      version='0.1',
      description='Python wrapper for OpenDevelop',
      author='Paris Kasidiaris',
      author_email='pariskasidiaris@gmail.com',
      url='http://opendevelop.sourcelair.com',
      packages=['opendevelop'],
      install_requires=requirements,
      license=open('LICENSE').read())
