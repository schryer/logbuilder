# Setup file to distribute isotopomer package using distutils.
from distutils.core import setup

prj = 'logbuilder'

setup(name=prj,
      version='1.0',
      description='Python package with basic tools that aid in logging Python projects.',
      author='David Schryer',
      author_email='schryer@ut.ee',
      url='http://www.tuit.ut.ee/',
      packages=[prj],
      )
