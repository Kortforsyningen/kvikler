"""
Setup script for the kvikler package.
"""

import os
import subprocess
from setuptools import setup

import kvikler

def readme():
    """
    Return a properly formatted readme text that can be used as the long
    description for setuptools.setup.
    """
    # This will fail if pandoc is not in system path.
    try:
        subprocess.call(['pandoc', 'readme.md', '--from', 'markdown', '--to', 'rst', '-s', '-o', 'readme.rst'])
        with open('readme.rst') as f:
            readme = f.read()
        os.remove('readme.rst')
        return readme
    except:
        return 'Geodetic database system for storarge of information on levelling observations and points.'

setup(
    name='kvikler',
    version=kvikler.__version__,
    description='Geodetic database system for storarge of information on levelling observations and points.',
    long_description=readme(),
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: ISC License (ISCL)',
      'Topic :: Scientific/Engineering :: GIS',
      'Topic :: Utilities'
    ],
    packages=['kvikler', 'kvikler.kvik'],
    entry_points = '''
        [console_scripts]
        kvik=kvikler.kvik.main:kvik

        [kvikler.kvik_commands]
        admin=kvikler.kvik.admin:admin
        kmsfile=kvikler.kvik.kmsfile:kmsfile
        gama=kvikler.kvik.gama:gama
    ''',
    keywords='levelling database geodesy',
    url='https://github.com/Kortforsyningen/kvikler',
    author='Kristian Evers',
    author_email='kreve@sdfe.dk',
    license='ISC',
    py_modules=['kvikler'],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'click',
        'click_plugins',
        'sqlalchemy',
    ],
)
