#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "click-spinner>=0.1.10",
    "ics>=0.7",
    "matplotlib>=3.2.1",
    "notebook>=6.0.3",
    "numpy>=1.18.3",
    "pandas>=1.0.3",
    "pyprojroot>=0.2.0",
    "seaborn>=0.10.1",
]

setup_requirements = ["pytest-runner", "ipython==7.13.0"]

test_requirements = [
    "pytest>=3",
    "pytest-mpl==0.11",
]

setup(
    author="Ricky Lim",
    author_email="rlim.email@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Calendar Heatmap",
    entry_points={"console_scripts": ["calh=calh.cli:cli",],},
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="calh",
    name="calh",
    packages=find_packages(include=["calh", "calh.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ricky-lim/calh",
    version="1.0.3",
    zip_safe=False,
)
