from setuptools import setup

setup(name = 'IBMQuantumExperience',
      packages = ['IBMQuantumExperience'], # this must be the same as the name above
      version='0.2',
      author='IBM Research Emergent Solutions',
      description='The official SDK to use IBM Quantum Experience in Python.',
      author_email='fmartinfdez@gmail.com',
      url = 'https://github.com/IBMResearch/python-api-client-quantum-experience',
      keywords = ['ibm', 'quantum computer', 'quantum experience'],
      license='MIT',
      install_requires=[
        'request'
      ],
      zip_safe=False)
