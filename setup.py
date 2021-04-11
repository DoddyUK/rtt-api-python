import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='rttapi',
    packages=find_packages(),
    version='0.1.0',
    description='Python wrapper for the Realtime Trains API',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Michael Dodd',
    license='MIT',
    test_suite='test'
)