# Towards Encoding Time in Text-Based Entity Embeddings


## Settings

Experiments were run using the following tools:

+ gensim 3.2.0 (using tensorflow has backend)
+ python 3.5
+ standard modules for math computation (numpy, pandas, sklearn and scipy)

## Data

Models can be downloaded from [here](http://inside.disco.unimib.it/download/federico/time-aware/), it contains:

+ The model for years entites
+ The skip-gram model for years
+ The baseline model (used in the experiments)

Gold Standards/Dataset used in the experiments are in the respective folder of this repository

## Code 

In the time_aware.py script you can find the main functions described in the paper. 

## Installation Instruction

Script can be used inside a virtualenv created with python3

```
virtualenv -p python3 envname
source envname/bin/activate


pip install gensim==3.2.0 

```






