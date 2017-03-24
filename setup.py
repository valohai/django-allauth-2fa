# -*- coding: utf-8 -*-

import codecs

from setuptools import setup, find_packages

def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

setup(
    name="django-allauth-2fa",
    version="0.4.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=1.8",
        "qrcode>=5.3",
        "django-allauth>=0.26.1",
        "django-otp>=0.3.5",
    ],
    author="Víðir Valberg Guðmundsson",
    author_email="valberg@orn.li",
    description="Adds two factor authentication to django-allauth",
    license="Apache 2.0",
    keywords=['otp', 'auth', 'two factor authentication', 'allauth', 'django', '2fa'],
    url="https://github.com/percipient/django-allauth-2fa",
    long_description=long_description(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'License :: OSI Approved :: Apache Software License',
    ],
)
