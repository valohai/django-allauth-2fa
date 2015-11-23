from setuptools import setup, find_packages

setup(
    name="django-allauth-2fa",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "django>=1.7.0",
        "qrcode==5.1",
        "django-allauth==0.23.0",
        "django-otp==0.3.1",
    ],
    author="Víðir Valberg Guðmundsson",
    author_email="valberg@orn.li",
    description="Adds two factor authentication to django-allauth",
    license="PSF",
    keywords="otp auth two factor authentication allauth django",
    url="https://github.com/percipient/django-allauth-2fa",
    long_description=open('README.rst', 'r').read(),
)
