# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

SRC_NAME: str = "pycaw"
REPO_NAME: str = "python-crypto-api-wrappers"

setuptools.setup(
    name="pycaw",
    version="0.0.1",
    author="Unique Divine",
    description=(
        "A Python package for wrapping common Crypto APIs like Etherscan,"
        " Messari, CoinGecko, FTMscan Coin Market Cap, etc."
    ),
    url="",
    project_urls={
        "Bug Tracker": f"https://github.com/Unique-Divine/{REPO_NAME}/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": SRC_NAME},
    packages=setuptools.find_packages(where=SRC_NAME),
    python_requires=">=3.9",
)
