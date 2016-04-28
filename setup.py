from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup


setup(
    name='omero-cli-duplicate',
    version='0.0.1',
    author='',
    author_email='',
    packages=['omero.plugins'],
    package_dir={"": "src"},
    url='',
    license='See LICENSE.txt',
    description='',
    long_description=open('README.txt').read(),
)
