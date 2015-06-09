# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    description = f.read()


setup(
    name='github-jenkins-proxy',
    version='0.1.0',
    packages=find_packages(),
    license=u'Apache license',
    url='https://github.com/mouadino/github-jenkins-proxy/',
    description=u'jenkins proxy to github',
    long_description=description,
    include_package_data=True,
    install_requires=[
        'flask',
        'python-jenkins',
        'requests',
        'giturlparse.py',
    ],
)
