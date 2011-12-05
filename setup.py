from distutils.core import setup
from notifications import __version__ as version

setup(
    name="django-generic-notifications",
    version=version,
    description="Generic notification system for Django, with multiple input types and output backends",
    long_description=open("README.rst").read(),
    author="Kevin Renskers",
    author_email="info@mixedcase.nl",
    url="https://github.com/kevinrenskers/django-generic-notifications",
    packages=[
        "notifications",
    ],
    install_requires=[
        "django >= 1.2",
    ],
    package_dir={"notifications": "notifications"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
