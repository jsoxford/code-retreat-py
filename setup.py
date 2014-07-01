# -*- coding: utf-8 -*-
"""
JS Oxford Code Retreat: Python Runner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage
-----

cr path/to/your/file.py

"""
from setuptools import setup


setup(
    name='code-retreat-py',
    version='0.1.0',
    url='http://github.com/jsoxford/code-retreat-py',
    license='MIT',
    author='George Hickman',
    author_email='george@ghickman.co.uk',
    description='Python Runner for JS Oxford\'s Code Retreat',
    long_description=__doc__,
    py_modules=['code_retreat.py'],
    entry_points={'console_scripts': ['cr=code_retreat:run']},
    install_requires=['pytest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
