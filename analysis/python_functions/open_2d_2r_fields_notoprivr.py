import numpy as np
import pandas as pd
import xarray as xr
import open_experiment as of

path='/scratch/wcq7pz/notebook/SM_paper/spatial_composites/'


sm_ti_c = xr.open_dataset(path+'/sm_ti_c_5deg_notoprivr.nc');
sm_ti_f = xr.open_dataset(path+'/sm_ti_f_5deg_notoprivr.nc');

deaccu_ti_c = xr.open_dataset(path+'/deaccu_ti_c_5deg.nc'); 
deaccu_ti_f = xr.open_dataset(path+'/deaccu_ti_f_5deg.nc'); 

sfc_ti_c = xr.open_dataset(path+'/sfc_ti_c_notopnorivr_5deg.nc'); 
sfc_ti_f = xr.open_dataset(path+'/sfc_ti_f_notopnorivr_5deg.nc'); 

sm_ti_3hb_c = xr.open_dataset(path+'/sm_ti_c_3hb_5reg_AB_notoprivr.nc');
sm_ti_3hb_f = xr.open_dataset(path+'/sm_ti_f_3hb_5reg_AB_notoprivr.nc');

deaccu_ti_3hb_c = xr.open_dataset(path+'/deaccu_ti_3hb_c_5deg_AB.nc'); 
deaccu_ti_3hb_f = xr.open_dataset(path+'/deaccu_ti_3hb_f_5deg_AB.nc'); 

sm_ti_6hb_c = xr.open_dataset(path+'/sm_ti_c_6hb_5reg_notoprivr.nc');
sm_ti_6hb_f = xr.open_dataset(path+'/sm_ti_f_6hb_5reg_notoprivr.nc');

deaccu_ti_6hb_c = xr.open_dataset(path+'/deaccu_ti_c_6hb_5reg_AB.nc'); 
deaccu_ti_6hb_f = xr.open_dataset(path+'/deaccu_ti_f_6hb_5reg_AB.nc'); 

sm_ti_12hb_c = xr.open_dataset(path+'/sm_ti_c_12hb_5reg_notoprivr.nc');
sm_ti_12hb_f = xr.open_dataset(path+'/sm_ti_f_12hb_5reg_notoprivr.nc');

deaccu_ti_12hb_c = xr.open_dataset(path+'/deaccu_ti_c_12hb_5reg_notoprivr.nc'); 
deaccu_ti_12hb_f = xr.open_dataset(path+'/deaccu_ti_f_12hb_5reg_notoprivr.nc');

sm_ti_24hb_c = xr.open_dataset(path+'/sm_ti_c_24hb_5reg_notoprivr.nc');
sm_ti_24hb_f = xr.open_dataset(path+'/sm_ti_f_24hb_5reg_notoprivr.nc');

deaccu_ti_24hb_c = xr.open_dataset(path+'/deaccu_ti_c_24hb_5reg_notoprivr.nc'); 
deaccu_ti_24hb_f = xr.open_dataset(path+'/deaccu_ti_f_24hb_5reg_notoprivr.nc');


sfc_ti_3hb_c = xr.open_dataset(path+'/sfc_ti_3hb_c_5deg_AB.nc');
sfc_ti_3hb_f = xr.open_dataset(path+'/sfc_ti_3hb_f_5deg_AB.nc'); 

sfc_ti_6hb_c = xr.open_dataset(path+'/sfc_ti_6hb_c_5deg_AB.nc');
sfc_ti_6hb_f = xr.open_dataset(path+'/sfc_ti_6hb_f_5deg_AB.nc'); 

sfc_ti_12hb_c = xr.open_dataset(path+'/sfc_ti_c_12hb_5reg_notoprivr.nc');
sfc_ti_12hb_f = xr.open_dataset(path+'/sfc_ti_f_12hb_5reg_notoprivr.nc'); 

sfc_ti_24hb_c = xr.open_dataset(path+'/sfc_ti_c_24hb_5reg_notoprivr.nc');
sfc_ti_24hb_f = xr.open_dataset(path+'/sfc_ti_f_24hb_5reg_notoprivr.nc'); 








