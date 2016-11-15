from setuptools import setup

setup(name = 'IBMQuantumExperience',
      packages = ['IBMQuantumExperience'], # this must be the same as the name above
      version='0.1.3',
      author='IBM Research Emergent Solutions',
      author_email='fmartinfdez@gmail.com',
      url = 'https://github.com/IBMResearch/python-sdk-quantum-experience',
      keywords = ['ibm', 'quantum computer', 'quantum experience'],
      license='MIT',
      install_requires=[
        'request',
        'logging'
      ],
      zip_safe=False)