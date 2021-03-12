# -*- coding: utf-8 -*-

import codecs

from setuptools import find_packages, setup


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name="django-allauth-2fa",
    version="0.8",
    packages=find_packages('.', include=('allauth_2fa', 'allauth_2fa.*')),
    include_package_data=True,
    install_requires=[
        "django>=1.11",
        "qrcode>=5.3",
        "django-allauth>=0.25",
        "django-otp>=0.3.12",
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
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires=">=3.6",
)
