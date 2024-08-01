Information related to the paper "Influence of soil moisture on the development of organized convective systems in South America" by Paccini and Schiro


1. Prepost
-----------
  - The runscript 'xce_remap_inidata' use the ICONtools (v 2.5.1) 
  for remaping initial data onto the model grid. Grids are obtained via the Online Grid Generator tool 
  provided by the German Meteorological Service (DWD) at https://webservice.dwd.de/cgi-bin/spp1167/webservice.cgi
  Access to the grid generator web service requires username/password. To this end, please contact icon@dwd.de
  The runscrip exp.run_nested starts the simulation with the ICON-NWP model (v 2.6.4) 
  These runscripts are adapted for the Levante HPC system (https://docs.dkrz.de/doc/levante). They are
  provided only for reference use.
  - Files remap_sa.h and grid_dom03p5.nc are used to process the model output. The bash script utilizes distance weighted average interpolation from Climate Data Operator (CDO, v 2.0.6) to remap the model output onto regular grids (NetCDF file).



2. Analysis
-----------
This directory contains python scripts and Jupyter notebooks that were used to process model output and observations, as well as to plot the manuscript Figures.
Some figures were edited (labelling and merging subplots) with the open source software Inkscape.
