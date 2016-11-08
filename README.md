# Python SDK IBM Quantum Experience

The official SDK to use [IBM Quantum Experience](https://quantumexperience.ng.bluemix.net/) in Python. 

This package can be use in [Jupyter Notebook](https://jupyter.org/).

* [Installation](#installation)
* [Getting Started](#getting-started)
* [Methods](#methods)
* [License](#license)
* [Reference](#reference)

## Installation

You can install me using `pip` or `easy_install`. For example, from the command line:

    $ pip install IBMQuantumExperience

### Getting Started

Now it's time to begin doing real work with Python and IBM Quantum Experience.

First, import our SDK:

```python
from IBMQuantumExperience import IBMQuantumExperience
```

Then, initialize your IBM Quantum Experience connection by supplying your *email* and *password*:

```python
api = IBMQuantumExperience("email@email.com", "p4Ssw0rD")
```

### Methods

#### Codes

To get the information of a Code, you only need the codeId:

```python
api.getCode("idCode")
```

#### Execution

To get all information (including the Code information) about a specific Execution of a Code, you only need the executionId:

```python
api.getExecution("idExecution")
```

To get only the Result about a specific Execution of a Code, you only need the executionId:

```python
api.getResultFromExecution("idExecution")
```

## License

MIT License

Copyright (c) 2016 IBM Research Emergent Solutions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Reference

[IBM Quantum Experience Tutorial](https://quantumexperience.ng.bluemix.net/qstage/#/tutorial?sectionId=c59b3710b928891a1420190148a72cce&pageIndex=0)

[IBM Quantun Experience Community](https://quantumexperience.ng.bluemix.net/qstage/#/community)