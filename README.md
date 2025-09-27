# KAlignedoscope: An interactive visualization tool for aligned clustering results from population structures analyses
Powered by JavaScript D3
## Feature Highlights
This tool aims to support user-interactivity and friendliness with aesthetic interface. There are three methods of reordering: by population, by dominant cluster of a selected mode, and by vertical cluster stacking order, with changes synced across all modes. There are several customizable features as well, including cluster name relabeling, cluster color picking, and title renaming. Users may also choose the visibility structure of minor modes and network connections when alignment cost and multi-modality is given. Beyond visual elements, information is also available through hovering tooltips across individuals' bars and above network connections. 
## Basic Usage

For installation, I will first assume that the user has Python installed (less custom to my tool, easier to write later). Users will also need to have the ```pandas`` package installed. If not, run in the terminal 
````
pip install pandas
````

## Install the KAlignedoscope package

Inside of the command line, write:
````
pip install kalignedoscope
````
It will be useful to download the example datasets and follow the available tutorial. It may be accessed below here: 
https://github.com/ramachandran-lab/KAlignedoscope/tree/a9c6dbadbb3e4174a99e456b3af78d39a7b46f91/Data

## To run KAlignedoscope on example dataset
Idea of how to explain this section nicely:
1. Explain what the data is, and how it is formatted
2. Confirm that they have installed it correctly and it is in the correct directory under the KAlignedoscope folder


Run the following lines in the terminal to initialize the tool:
````
python -m kalignedoscope 
--membership_folder Data/Cape_Verde_Data 
--alignment_file Data/Cape_Verde_Alignment.txt 
````
For help and more options write in the command line:
````
pythom -m kalignedoscope -h
````
## Processing outputs from other tools
This tool primarily functions as a visualization and data navigation tool for alignment results, which may be created from running existing packages such as CLUMPPLING or PONG. These results may need to be processed before the datasets are fed into CLUMPICK. Two python functions are provided to assist with preparing data.



### Notes on Running Directly from Clummpling Output Directory
We will need three files: modes_aligned folder, alignment_acrossK_avg.txt file, and ind_labels_grouped.txt file. To make the formatting usuable for our tool you will need to first run it through processFromExternal.py (need to make a output folder path for it to put the sorted data into), then addPopulation.py where you need to use the ind_labels_grouped.txt file (which you should first paste into a .CSV file under a column that matches case with "Population") to add another column to all the datasets. Then the data is ready to be used, but you may want to read in your alignment cost file as well, which should be processed through the convertAligned.py function (which just reads it into CSV format). 

### File input formatting 
#### Title 
KAlignedoscope reads each table as an individual structure plot, as such, the user should tuck all their .Q matrices or processed .CSV files into the data folder under **KAlignedoscope**. Due to the particular nature of this tool that relies on detecting particular K modes and M clusters for layout, each file in the folder should be consistently named with information that must be included in the title: **K** = X Clusters and **M** = Y Modes. For example: ````YourName_KXMY.Q````



#### Data Layout
There should be a name column, optional population column, and $K$ amount of columns for the cluster proportions. It should be noted that the number of of $K$ clusters for each file should be matched across file name and number of cluster columns. If the user decides to use the ````processFromExternal.py```` function they will be safe on the formatting, otherwise the user should be sure their columns are named particularly (matching case): **name, Population, Cluster1, Cluster2...** and so on. Sum of clusters for each individual should be 1.  

!!! Consider putting an image or table here to demonstrate?

### Alignment Data
Alignment data is used to render across-K edges in the Network Connections feature. Designed to read directly from Clumppling's results, which users should download the **alignment_acrossK.txt** file by navigating to the output folder in Clumppling's directory after performing a sucessful run of the program. Otherwise, it is important to format files in the following for compatibility with KAlignedoscope. 

For example, this is the top three rows of Cape Verde alignment data from Clumppling's outout. Please be sure to format as **Mode1-Mode2**. 

| Mode1-Mode2 | Cost                  |
|-------------|-----------------------|
| K4M1-K5M1   | 0.0042625183996884055 |
| K4M2-K5M1   | 0.06438957610509989   |
| K4M1-K5M2   | 0.005455565400171093  |


### processFromExternal.py
which matches case and title structures, converting from .Q matrice file shapes. 
### addPopulation.py
which adds a Population column if given. 
### convertAligned.py
