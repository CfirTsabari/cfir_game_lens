"""
Setup file for cfir game lens
"""
import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    """
    Read file.
    """
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as read_file:
        return re.sub(
            text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), read_file.read()
        )


setup(
    name="cfir_game_lens",
    version="0.1.0",
    url="NO_URL_::",
    license="MIT",
    author="Cfir Tsabari",
    author_email="cfir.tsabari@gmail.com",
    description="A tool that analyze game covers using OpenCV",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
