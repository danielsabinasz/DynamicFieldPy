from setuptools import setup, find_packages

setup(name='DynamicFieldPy',
      version='0.1.1',
      python_requires='>3.5',
      description='A library for creating Dynamic Field architectures with Python',
      url='https://github.com/danielsabinasz/DynamicFieldPy',
      author='Daniel Sabinasz',
      author_email='daniel@sabinasz.net',
      license='CC-BY-ND 3.0',
      packages=find_packages(include=['dfpy', 'dfpy.*']),
      install_requires=[
          'pillow==9.2.0'
      ],
      zip_safe=False)
