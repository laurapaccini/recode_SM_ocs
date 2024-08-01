import numpy as np
import pandas as pd
import xarray as xr
import open_experiment as of
import tools_for_evolution as tools


# Disable a few warnings:
import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)
warnings.filterwarnings('ignore', category=RuntimeWarning, append=True)
warnings.filterwarnings('ignore', category=FutureWarning, append=True)
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)


path='/scratch/wcq7pz/'

### read Stage info
df_ocs_control_AB = pd.read_pickle('pkl_files/df_ocs_control_AB.pkl'); 
df_ocs_fixedSM_AB = pd.read_pickle('pkl_files/df_ocs_fixedSM_AB.pkl'); 


### Add direction propagations in simulations

df_stage_c = df_ocs_control_AB.groupby('cell').apply(tools.calculate_direction).reset_index(drop=True)
df_stage_f = df_ocs_fixedSM_AB.groupby('cell').apply(tools.calculate_direction).reset_index(drop=True)

df_stage_c['categorized_direction'] = df_stage_c['direction'].apply(tools.categorize_direction)
df_stage_f['categorized_direction'] = df_stage_f['direction'].apply(tools.categorize_direction)


##Read near environment SM conditions

#Read 2 times radio distance:
sm_env_c_2r = pd.read_pickle('pkl_files/sm_env_all_c_2r_notoprivr.pkl')
sm_env_f_2r = pd.read_pickle('pkl_files/sm_env_all_f_2r_notoprivr.pkl')


## Add information to dataframes
df_2r_c_i = tools.add_stdvar_to_df(sm_env_c_2r.std_SM_env.reset_index(drop=True),
                                 df_stage_c[(df_stage_c.longitude>-76.5)&(df_stage_c.longitude<-55.5)],stage='t_i',aver=False);

df_2r_f_i = tools.add_stdvar_to_df(sm_env_f_2r.std_SM_env.reset_index(drop=True),
                                 df_stage_f[(df_stage_f.longitude>-76.5)&(df_stage_f.longitude<-55.5)],stage='t_i',aver=False);


    











