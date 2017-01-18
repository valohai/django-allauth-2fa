# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="django-allauth-2fa",
    version="0.4.3",
    packages=find_packages(),
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
    keywords="otp auth two factor authentication allauth django",
    url="https://github.com/percipient/django-allauth-2fa",
    long_description=open('README.rst', 'r').read(),
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
        'Framework :: Django',
        'License :: OSI Approved :: Apache Software License',
    ],
)
