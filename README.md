## Sampling Our Kets Randomly and Accurately using Tensor networks

SourKRAUT is a quantum simulator that can be used to generate thousands of samples 
for various models. This data is generated using unitary tensor network calculations. 
It can additionally be used to store amplitudes and values of physical observables. 
Once the data is generated, the results can be verified
using histograms and relative error plots for various observables.
More details can be found in the Quantum Sampling summary under the docs folder.

## Getting Started

To use SourKRAUT, you will need to install [ITensor](http://itensor.org/). 
ITensor is a C++ library for implementing tensor network calculations.
The instructions for installing ITensor are outlined on their home page.
To install SourKRAUT, you will need to clone this repository. This can
be done by typing the following command:

```bash
git clone git@github.com:MelkoCollective/SourKRAUT.git
```

One can follow the Example.py file or the jupyter notebook in the examples
folder for additional guidance on using SourKRAUT.
