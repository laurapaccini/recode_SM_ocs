import xarray as xr
import pandas as pd
import os

## Function to open multiple files
def open_experiment(exp_folder_name, start_file, end_file, file_name,ext='.nc',datavars=False,dv=''):
    """Simple function to open netcdf files as one dataset object in xarray"""

    ##depending on the data format change '%02d' - ''%06d'
    folder_list = ['%02d' % m for m in range(start_file, end_file+1)] 
    files = [exp_folder_name+ '/' + file_name + folder_list[i] +ext for i in range(len(folder_list))] 
    files_exist=[os.path.isfile(s) for s in files]

    if not(all(files_exist)):
        raise EOFError('EXITING BECAUSE OF MISSING FILES', [files[elem] for elem in range(len(files_exist)) if not files_exist[elem]])
    
    
    if datavars==True:
        ds = xr.open_mfdataset(files, combine='by_coords')[dv]
    else:
        ds = xr.open_mfdataset(files,combine='by_coords') 

    return ds

## Function to update lon coordinate
def update_lon(ds,longitude='lon'):
    ds.coords[longitude] = (ds.coords[longitude] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)
    return ds

path='/scratch/wcq7pz/exp_levante_post/'

## Accumulated variables
#Control experiment
control_accu = open_experiment(path+'control_d1pc/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
control_deaccu1 = control_accu.diff('time'); del(control_accu)

control_accu = open_experiment(path+'m2_control/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
control_deaccu2 = control_accu.diff('time'); del(control_accu)

control_accu = open_experiment(path+'m3_control/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
control_deaccu3 = control_accu.diff('time'); del(control_accu)

#FixedSM experiment
fixedSM_accu = open_experiment(path+'fixedSM_d1pc/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
fixedSM_deaccu1 = fixedSM_accu.diff('time'); del(fixedSM_accu)

fixedSM_accu = open_experiment(path+'m2_fixedSM/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
fixedSM_deaccu2 = fixedSM_accu.diff('time'); del(fixedSM_accu)

fixedSM_accu = open_experiment(path+'m3_fixedSM/',30,49,'ICON_nested_accu_DOM03_5km_',ext='_reg.nc')
fixedSM_deaccu3 = fixedSM_accu.diff('time'); del(fixedSM_accu)

##Land variables
control_land1 = open_experiment(path+'control_d1pc/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])
fixedSM_land1 = open_experiment(path+'fixedSM_d1pc/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])

control_land2 = open_experiment(path+'m2_control/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])
fixedSM_land2 = open_experiment(path+'m2_fixedSM/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])

control_land3 = open_experiment(path+'m3_control/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])
fixedSM_land3 = open_experiment(path+'m3_fixedSM/',30,49,'ICON_nested_2Dland_DOM03_5km_',ext='_reg.nc',datavars=True,dv=['w_so'])

##Surface variables
listvars = ['tqv_dia','cape_ml','u_10m','v_10m','t_g','qv_s','qv_2m','t_2m','pres_sfc','clct']
#listvars = ['qv_2m','pres_msl','cin_ml','t_2m','td_2m','pres_sfc']
control_sfc1 = open_experiment(path+'control_d1pc/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)
fixedSM_sfc1 = open_experiment(path+'fixedSM_d1pc/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)

control_sfc2 = open_experiment(path+'m2_control/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)
fixedSM_sfc2 = open_experiment(path+'m2_fixedSM/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)

control_sfc3 = open_experiment(path+'m3_control/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)
fixedSM_sfc3 = open_experiment(path+'m3_fixedSM/',30,49,'ICON_nested_2Dsfc_DOM03_5km_',ext='_reg.nc',datavars=True,dv=listvars)


#Define new date ranges to attach members
ti = '2017-3-31T02:00'; tf = '2017-4-19T23:00'; tf2 = '2017-4-19T23:00'
dti2 =pd.date_range(start='2018-03-31 02:00',end='2018-04-19 23:00', freq='1H');
dti3 =pd.date_range(start='2019-03-31 02:00',end='2019-04-19 23:00', freq='1H')

##Uptade times 
control_deaccu2 = control_deaccu2.sel(time=slice(ti,tf)); control_deaccu2 = control_deaccu2.update({"time": ("time", dti2)}) ; 
control_deaccu3 = control_deaccu3.sel(time=slice(ti,tf)); control_deaccu3 = control_deaccu3.update({"time": ("time", dti3)});
fixedSM_deaccu2 = fixedSM_deaccu2.sel(time=slice(ti,tf)); fixedSM_deaccu2 =fixedSM_deaccu2.update({"time": ("time", dti2)}); 
fixedSM_deaccu3 = fixedSM_deaccu3.sel(time=slice(ti,tf)); fixedSM_deaccu3 =fixedSM_deaccu3.update({"time": ("time", dti3)});

control_land2 = control_land2.sel(time=slice(ti,tf)); control_land2 = control_land2.update({"time": ("time", dti2)}) ; 
control_land3 = control_land3.sel(time=slice(ti,tf)); control_land3 =control_land3.update({"time": ("time", dti3)});
fixedSM_land2 = fixedSM_land2.sel(time=slice(ti,tf)); fixedSM_land2 =fixedSM_land2.update({"time": ("time", dti2)}); 
fixedSM_land3 = fixedSM_land3.sel(time=slice(ti,tf)); fixedSM_land3 =fixedSM_land3.update({"time": ("time", dti3)});

control_sfc2 = control_sfc2.sel(time=slice(ti,tf)); control_sfc2 = control_sfc2.update({"time": ("time", dti2)}) ; 
control_sfc3 = control_sfc3.sel(time=slice(ti,tf)); control_sfc3 =control_sfc3.update({"time": ("time", dti3)});
fixedSM_sfc2 = fixedSM_sfc2.sel(time=slice(ti,tf)); fixedSM_sfc2 =fixedSM_sfc2.update({"time": ("time", dti2)}); 
fixedSM_sfc3 = fixedSM_sfc3.sel(time=slice(ti,tf)); fixedSM_sfc3 =fixedSM_sfc3.update({"time": ("time", dti3)});


##Concatenate members
control_deaccu = xr.concat([control_deaccu1.sel(time=slice(ti,tf)),control_deaccu2,control_deaccu3],'time')
fixedSM_deaccu = xr.concat([fixedSM_deaccu1.sel(time=slice(ti,tf)),fixedSM_deaccu2,fixedSM_deaccu3],'time')

control_land = xr.concat([control_land1.sel(time=slice(ti,tf)),control_land2,control_land3],'time')
fixedSM_land = xr.concat([fixedSM_land1.sel(time=slice(ti,tf)),fixedSM_land2,fixedSM_land3],'time')

control_sfc = xr.concat([control_sfc1.sel(time=slice(ti,tf)),control_sfc2,control_sfc3],'time')
fixedSM_sfc = xr.concat([fixedSM_sfc1.sel(time=slice(ti,tf)),fixedSM_sfc2,fixedSM_sfc3],'time')

control_land = xr.concat([control_land1.sel(time=slice(ti,tf)).w_so.to_dataset(name='w_so'),
                          control_land2.w_so.to_dataset(name='w_so'),control_land3.w_so.to_dataset(name='w_so')],'time')
fixedSM_land = xr.concat([fixedSM_land1.sel(time=slice(ti,tf)).w_so.to_dataset(name='w_so'),
                          fixedSM_land2.w_so.to_dataset(name='w_so'),fixedSM_land3.w_so.to_dataset(name='w_so')],'time')

##Update longitude
control_deaccu = update_lon(control_deaccu); fixedSM_deaccu = update_lon(fixedSM_deaccu);
control_land = update_lon(control_land); fixedSM_land = update_lon(fixedSM_land)
control_sfc = update_lon(control_sfc); fixedSM_sfc = update_lon(fixedSM_sfc)

