#!/usr/bin/env python

""" Setup for met_test """

from glob import glob
from setuptools import find_packages, setup
from os.path import basename, dirname, realpath

def main():
    return setup(
        author='Forecasting Research group',
        author_email='Sijin.Zhang@metservice.com',
        data_files=[('met_test/test', glob('test/*'))],
        description='Script for verification',
        maintainer='Forecasting Research group',
        maintainer_email='research@metservice.com',
        # Use name of the directory as name
        name=basename(dirname(realpath(__file__))),
        scripts=['scripts/run_conv.py'],
        packages=find_packages(),
        zip_safe=False
    )

if __name__ == '__main__':
main()
