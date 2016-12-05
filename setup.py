import os
import subprocess
from setuptools import setup, find_packages

setup(
    name="flask_modular_auth",
    version="0.2",
    packages=find_packages(),
    install_requires=['flask', ]
)
