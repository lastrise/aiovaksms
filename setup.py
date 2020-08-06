# -*- coding: utf-8 -*-
from setuptools import setup

"""
@author: lastrise
@contact: github
@license Apache License, Version 2.0, see LICENSE file
Copyright (C) 2019
"""


def requirements():
    """Build the requirements list for this project"""
    requirements_list = list()
    with open('requirements.txt') as pc_requirements:
        for install in pc_requirements:
            requirements_list.append(install.strip())
    return requirements_list


setup(
    name='aiovaksms',
    version='1.0.0',
    long_description="",
    long_description_content_type='text/markdown',
    description='Async wrapper for automatic reception of SMS-messages by vak-sms.com',
    author='lastrise',
    license='Apache License, Version 2.0, see LICENSE file',
    keywords='sms, recive, vak-sms.com, autoreg',
    author_email='my_mail@mail.ru',
    url='https://github.com/lastrise/aiovaksms/',
    download_url='https://github.com/lastrise/aiovaksms/archive/master.zip',
    packages=['aiovaksms'],
    install_requires=requirements(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ])
