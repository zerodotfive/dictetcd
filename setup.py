#!/usr/bin/env python

from distutils.core import setup

setup(
    name='dictetcd',
    version='0.1',
    packages=['dictetcd'],
    scripts=['bin/etcd-dump', 'bin/etcd-restore'],
    url='https://github.com/zerodotfive/dictetcd',
    install_requires=[
        'python-etcd'
    ],
    license='BSD',
    author='zerodotfive'
)
