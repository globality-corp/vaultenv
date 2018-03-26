#!/usr/bin/env python
from setuptools import find_packages, setup


project = "vaultenv"
version = "0.2.0"

setup(
    name=project,
    version=version,
    description="Ansible vault environment variable exporting",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/vaultenv",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    keywords="vaultenv",
    install_requires=[
        "ansible>=2.5.0",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    entry_points={
        "console_scripts": [
            "vaultenv = vaultenv.main:main"
        ],
    },
    tests_require=[
        "coverage>=4.5.1",
        "PyHamcrest>=1.9.0",
    ],
)
