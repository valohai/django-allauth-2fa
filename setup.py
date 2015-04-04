from setuptools import setup, find_packages

setup(
    name="django-allauth-2fa",
    version="0.1",
    packages=find_packages(exclude=['testproject']),
    install_requires=[
        package for package in open('requirements.txt', 'r').readlines()
    ],

    author="Víðir Valberg Guðmundsson",
    author_email="valberg@orn.li",
    description="Adds two factor authentication to django-allauth",
    license="PSF",
    keywords="otp auth two factor authentication allauth django",
    url="https://github.com/valberg/django-allauth-2fa",

    long_description=open('README.rst', 'r').read(),
)
