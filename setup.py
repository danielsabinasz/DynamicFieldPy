from setuptools import setup

setup(name='DynamicFieldPy',
      version='0.1',
      description='A library for creating Dynamic Field architectures with Python',
      url='https://github.com/danielsabinasz/DynamicFieldPy',
      author='Daniel Sabinasz',
      author_email='daniel@sabinasz.net',
      license='CC-BY-ND 3.0',
      packages=['dfpy'],
      install_requires=[
          'pillow'
      ],
      zip_safe=False)
