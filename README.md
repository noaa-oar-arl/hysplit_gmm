# hysplit_gmm
This repository is supplemental material for the publication

### Dependencies
https://github.com/noaa-oar-arl/monetio  
https://github.com/noaa-oar-arl/utilhysplit  

## Contents
### Directories
#### RunFiles Directory
    Contains subdirectories with CONTROL and SETUP.CFG files for HYSPLIT runs.  
    The CONTROL file expects to find metdata in the Data directory.  
    The metdata is not included in the repository.  
    WRF dta can be obtained from the ARL archive https://www.ready.noaa.gov/archives.php.
    ERA5 data can be obtained and converted to ARL format as described here https://github.com/amcz/hysplit_metdata.

#### Data directory
    Contains text files with observations for the tracer experiments.  

#### txtfiles directory
    Contains text files with model results for the tracer experiments.

#### FigureScripts directory
    Contains bash scripts for creating multi panel figures.

### Jupyter Notebooks

#### captex1_notebook.ipynb
    This notebook creates the panels for Figures 1 and 2. It also creates figures which are not shown in the paper.
#### Figure3.ipynb  
    This notebook creates Figure 3.
#### Figure4and5and6.ipynb
#### Figure7and8.ipynb
#### Figure9.ipynb
