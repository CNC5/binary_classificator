import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "binary_classificator",
    version = "0.1",
    author = "CNC5",
    description = ("Natural language binary classificator with a wrapper"),
    license = "BSD-3",
    url = "https://github.com/CNC5/binary_classificator",
    packages=['binary_classificator'],
    long_description=read('README.md'),
    install_requires=[
        'tensorflow',
        'numpy',
        'setuptools'
    ]
)
