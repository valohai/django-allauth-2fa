# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="django-allauth-2fa",
    version="0.1.4",
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
    license="PSF",
    keywords="otp auth two factor authentication allauth django",
    url="https://github.com/percipient/django-allauth-2fa",
    long_description=open('README.rst', 'r').read(),
)
