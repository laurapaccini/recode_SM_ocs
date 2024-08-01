import numpy as np
import pandas as pd


def add_stdvar_to_df(dataset,dataframe,var='w_so',varname='SM_std_env',stage='t_i',aver=True):
    """
    dataset: 3d or 2D dataset if aver==True, otherwise could be a dataframe
    """
    new_df = dataframe[dataframe.stage==stage].reset_index()
    
    if aver==True:
        ave_var = dataset[var].std(['lat','lon']);
        new_df[varname] = ave_var
    else:
        new_df[varname] = dataset
        
    return(new_df)
        

def add_stage_convective_system(df_tracked):
    """
    Two main stages are initial t_i and t_f correspondent to first and last timesteps. Intermediate stages
    are denoted t_1, t_2,..,t_n
    """
    df = df_tracked[['cell','time_cell']].copy()

    # count the number of stages for each cell
    n_stages = df.groupby('cell')['time_cell'].count() - 1

    # create a dictionary of stages for each cell
    stages_dict = {}
    for cell in n_stages.index:
        stages_dict[cell] = ['t_i'] + [f"t_{i}" for i in range(1, n_stages.loc[cell])] + ['t_f']

    # create a new column 'stage' based on the cell and the stages dictionary
    df['stage_n'] = [stages_dict[df.loc[i, 'cell']][df.groupby('cell').cumcount()[i]] for i in range(len(df))]
    
    dfn = df_tracked.reset_index(drop=True);
    dfn['stage_n'] = df['stage_n']

    return(dfn)


def calculate_direction(df):
    # Calculate the time difference in hours
    df['time_diff_hours'] = df['time_cell'].diff().dt.total_seconds() / 3600.0

    # Calculate the change in latitude and longitude
    df['delta_lat'] = df['latitude'].diff()
    df['delta_lon'] = df['longitude'].diff()

    # Calculate the direction as an angle in degrees
    df['direction'] = np.arctan2(df['delta_lat'], df['delta_lon']) * 180 / np.pi

    # Replace NaN values in direction column with 0 (or any other desired value)
    #df['direction'].fillna(0, inplace=True)
    
    # Convert direction angles into cardinal directions
    def angle_to_direction(angle):
        if pd.notna(angle):
            if np.round(angle,1) >= -45 and np.round(angle,1) < 45:
                return 'E'
            elif np.round(angle,1) >= 45 and np.round(angle,1) < 135:
                return 'N'
            elif np.round(angle,1) >= -135 and np.round(angle,1) < -45:
                return 'S'
            else:
                return 'W'
            
        else:
            return np.nan  # Retain NaN values

    df['cardinal_direction'] = df['direction'].apply(angle_to_direction)

    return df

# Function to categorize angles into directions
def categorize_direction(angle):
    if pd.notna(angle):
        if angle >= -22.5 and angle < 22.5:
            return 'E'
        elif angle >= 22.5 and angle < 67.5:
            return 'NE'
        elif angle >= 67.5 and angle < 112.5:
            return 'N'
        elif angle >= 112.5 and angle < 157.5:
            return 'NW'
        elif angle >= 157.5 or angle < -157.5:
            return 'W'
        elif angle >= -157.5 and angle < -112.5:
            return 'SW'
        elif angle >= -112.5 and angle < -67.5:
            return 'S'
        elif angle >= -67.5 and angle < -22.5:
            return 'SE'
    else:
        return np.nan

    
    

### For plots


def sel_sizes(ds,df,cond_var='area_ob',var='',cond_valu=10e3,cond_vall=7e3,lim1=-100,lim2=100):
    """
    sel_var = ds.sel(time=df[(df[cond_var]>cond_vall)&(df[cond_var]<cond_valu)]['index'].tolist())[var].sel(lon=slice(lim1,lim2),lat=slice(lim1,lim2));
    """
    
    sel_var = ds.sel(time=df[(df[cond_var]>cond_vall)&(df[cond_var]<cond_valu)]['index'].tolist())[var].sel(lon=slice(lim1,lim2),lat=slice(lim1,lim2));
    
    return(sel_var)




def select_SM_topo_region(df,ds,topo_var='topo_median',c_var='cardinal_direction',topo_lim=100,cd='',lati='',latf='',
                         loni='',lonf=''):
    """
    df = dataframe with all cases of given exeperiment (control or fixedSM)
    ds = dataset from which the specific cases will be selected
    stage = "t_i", 't_i' or 't_f' referreing to the stage of the ocnvective system
    c_var = conditional variable, default: 'SM_std_env' standard deviation of sorrounding environment
    lim = threshold value of c_var
    time = if "all" consider all time, other options are "more than" or "less_than" a specific hour
    t = if time is set "more than" or "less_than", then is the hour according to the local time.
    cd=cardinal direction
    """
      
    new_cond = (df[topo_var]<=topo_lim)&(df[c_var]==cd)&(df['latitude']<latf)&(df['latitude']>lati)&(df['longitude']>loni)&(df['longitude']<lonf) 
    new_ds = ds.sel(time = new_cond.tolist())
    

    return(new_ds,df[new_cond].drop(columns=['level_0','index']).reset_index())