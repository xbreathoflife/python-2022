import setuptools
from setuptools import setup

setup(
    name="ast_fib",
    version="1.3",
    author="Aleksandra Obriadina",
    author_email="xbreathoflife@gmail.com",
    url="https://github.com/xbreathoflife/python-2022",
    long_description_content_type="text/markdown",
    install_requires=[
        "matplotlib==3.5.1",
        "networkx==2.6.3",
        "pydot==1.4.2",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)