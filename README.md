# Towards Encoding Time in Text-Based Entity Embeddings


## Settings

Experiments were run using the following tools:

+ gensim 3.2.0 (using tensorflow has backend)
+ python 3.5
+ standard modules for math computation (numpy, pandas, sklearn and scipy)

## Data

Models can be downloaded from [here](http://inside.disco.unimib.it/download/federico/time-aware/), the tar file contains:

+ The model for years entites
+ The skip-gram model for entities
+ The baseline model (used in the experiments)

Gold Standards/Dataset used in the experiments are in the respective folder of this repository

## Code 

In the time_aware.py script you can find the main functions described in the paper. 

### Helper Function

in the utilities folder you can find two scripts that can be used to generate the data you need. The
 `temporal_data_generation.py` allows you to extract the temporal descriptions from Wikipedia while the 
  `generate_embeddings_for_years.py` will allow you to generate the embeddings for the year from the temporal 
  description and a given model.
  
#### Example of Usage
  
+ `python temporal_data_generation.py -sy 1900 -ey 2000 -an 1` 
	+ This command will generate the temporal descriptions from 1900 to 2000 and it will annotate them using DBpedia Spotlight.
You can also non annotate them and use a general word embedding model in the next step
+ `python generate_embeddings_for_years.py --embeded /location/of/gensim.model --dim 100 --an /location/of/years/description/folder -em /location/of/the/output/file/you/want/to/generate.txt`
	+ This command will generate the 100 dimensional embeddings for temporal entities from the embedded model
 (note that the dimension should be the same as the one used in the embedded model. We use gensim to load the model).
  
  


## Installation Instruction

Script can be used inside a virtualenv created with python3

```
virtualenv -p python3 envname
source envname/bin/activate


pip install gensim==3.2.0 

```






