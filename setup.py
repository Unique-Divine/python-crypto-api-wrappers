#!/usr/bin/env python
# Copyright Unique Divine
#
# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

SRC_NAME: str = "pycaw"
REPO_NAME: str = "python-crypto-api-wrappers"

setuptools.setup(
    name="python-caw",
    version="0.0.1",
    author="Unique Divine",
    description=(
        "A Python package for wrapping common Crypto APIs like Etherscan,"
        " Messari, CoinGecko, FTMscan Coin Market Cap, etc."
    ),
    url="",
    project_urls={
        "Bug Tracker": f"https://github.com/Unique-Divine/{REPO_NAME}/issues",
        "Source Code": f"https://github.com/Unique-Divine/{REPO_NAME}",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests*"]),
    include_package_data=True, 
    python_requires=">=3.9",
)
