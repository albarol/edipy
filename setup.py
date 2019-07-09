import os
import re

from setuptools import setup, Command


here = os.path.abspath(os.path.dirname(__file__))


version = "0.0.0"
with open(os.path.join(here, "CHANGES.md")) as versions:
    for line in versions:
        version = line.strip()
        if re.search(r'^[0-9]+\.[0-9]+(\.[0-9]+)?$', version):
            break


def readme():
    with open("README.md") as readme:
        return readme.read()


class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
            pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)



setup(name='edipy',
      version=version,
      description='Parser positional files',
      long_description=readme(),
      url='https://github.com/fakeezz/edipy',
      author='fakeezz',
      author_email='fakeezz@gmail.com',
      license='MIT',
      packages=['edipy'],
      classifiers=[
        'Programming Language :: Python'
      ],
      cmdclass={'version': VersionCommand},
)
