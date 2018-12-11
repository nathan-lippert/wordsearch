""" For building wordsearch package """

from setuptools import setup, find_packages


VERSION = "1.0"

setup(
    name="wordsearch",
    version=VERSION,
    packages=find_packages(),
    entry_points={"console_scripts": ["wordsearch = wordsearch.__main__:main"]},
)
