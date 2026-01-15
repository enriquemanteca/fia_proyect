# Genetic Algorithm vs Multi-Start Local Search

This repository contains the source code, datasets, and generation scripts for the FIA project focused on solving the **Travelling Salesman Problem (TSP)**. Two Artificial Intelligence paradigms are implemented and compared: a **Genetic Algorithm (GATSP)** and a **Multi-Start Local Search (MSLSTSP)**.

The project evaluates the performance of both algorithms on standard instances (Symmetric/Euclidean) and on synthetic scenarios with asymmetry and noise.

## Miembers

Enrique Manteca Sánchez
Miguel Costales González
---

## Structure of the repository


```text
.
├── data/
│   ├── tsplib/               # Original instances (.tsp) from TSPLIB (Ulysses22, Berlin52, etc.)
│   └── generated/            # Synthetic instances with noise and asymmetry
├── src/ 
│   ├── tsplib_reader.py      # Parser for reading standard .tsp files
│   ├── noise.py              # Stochastic noise injection module
│   ├── asymetry.py           # Transformation of symmetric matrices to directed matrices (Asymmetry)
│   ├── distance.py           # Abstraction layer for cost calculation
│   └── generate_instances.py # Script for creating test datasets
├── GATSP.py                  # Implementation of the Genetic Algorithm
├── MSLSTSP.py                # Implementation of Multi-start Local Search
├── utils.py                  # Auxiliary functions (Graphics, I/O, metrics)
└── README.md                 # Project documentation



```

## Replication of executions

To execute the algorithms, you must enter the GATSP.py or MSLSTSP.py file, depending on the algorithm you want to execute, and you must enter the instance you want to execute in both the filename variable (.tsp file) and in the code location with open(‘.json’).
For the instance of n=1000, you cannot enter the address in the filename variable, as there is no .tsp file for it.

You can also change the parameters of both algorithms in the variables at the end of the code.