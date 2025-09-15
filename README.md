# Clumpick: An interactive visualization tool for aligned clustering results from population structures analyses
Powered by JavaScript D3
## Feature Highlights
This tool aims to support user-interactivity and friendliness with aesthetic interface. There are three methods of reordering: by population, by dominant cluster of a selected mode, and by vertical cluster stacking order, with changes synced across all modes. There are several customizable features as well, including cluster name relabeling, cluster color picking, and title renaming. Users may also choose the visibility structure of minor modes and network connections when alignment cost and multi-modality is given. Beyond visual elements, information is also available through hovering tooltips across individuals' bars and above network connections. 
## Basic Usage

For installation, I will first assume that the user has Python installed (less custom to my tool, easier to write later). 

## Install the Clumpick package

Inside of the command line, write:
````
pip install clumpick
````
It will be useful to download the example datasets and follow the available tutorial. It may be accessed below here: 
https://github.com/ramachandran-lab/Clumpick/tree/a9c6dbadbb3e4174a99e456b3af78d39a7b46f91/Data

## To run Clumpick on example dataset
Idea of how to explain this section nicely:
1. Explain what the data is, and how it is formatted
2. Confirm that they have installed it correctly and it is in the correct directory under the Clumpick folder
3. 
Run the following lines in the terminal to initialize the tool:
````
python -m clumpick \
--membership_folder Data/Cape_Verde_Data \
--alignment_file Data/Cape_Verde_Alignment.txt 
````
