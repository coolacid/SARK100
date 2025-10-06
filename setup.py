#!/usr/bin/env python3
"""Setup script for pysark100 package."""

from setuptools import setup, find_packages


# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name="pysark100",
    version="1.0.0",
    author="Jason Kendall (VE3YCA)",
    author_email="ve3yca@ve3yca.com",  # Add your email here
    description="Python Library and Tools for the SARK100 SWR Analyzer",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/coolacid/SARK100",
    project_urls={
        "Bug Tracker": "https://github.com/coolacid/SARK100/issues",
        "Documentation": "https://github.com/coolacid/SARK100",
        "Source Code": "https://github.com/coolacid/SARK100",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "sark100=pysark100.cli.sark100:main",
        ],
    },
    keywords=[
        "sark100",
        "swr",
        "antenna",
        "analyzer",
        "ham radio",
        "amateur radio",
        "rf",
        "measurement",
        "impedance",
        "radio frequency",
    ],
    include_package_data=True,
    zip_safe=False,
    license="GNU Affero General Public License v3.0 or later (AGPL-3.0+)",
)