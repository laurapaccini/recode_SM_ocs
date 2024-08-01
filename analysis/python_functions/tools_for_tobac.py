from scipy import ndimage
import numpy as np
import pandas as pd

def mask_var(array,arrayvar,grid_size,rr_limit=0,stats=True, 
                  s = ndimage.generate_binary_structure(2,2),lon1='',lat1='',timeds=''):
    """
    array: 3D array (time,lat,lon)
    grid_size: array with area information about the grid (cdo griddarea)
    rr_limit: threshold for precipitation rate before selecting the objects, default 1 mm hr-1
    s = structuring element that defines feature connections, default 8 way connection
    """
    pr_binary = np.zeros(np.shape(array))
    pr_binary[array>rr_limit] = 1
    
    lw=np.empty_like(pr_binary,dtype='int32'); num=np.empty_like(np.squeeze(pr_binary[:,0,0]),dtype='int32')
    for i in range(np.size(pr_binary,0)):
        lw[i,:,:],num[i] = ndimage.label(pr_binary[i,:,:],structure=s)
    indices_n = [np.arange(np.max(lw[i,:,:])+1) for i in range(np.size(lw,0)) ]
    ## clear and rename labels (after threshold)
    labels = [np.unique(lw[i,:,:]) for i in range(np.size(lw,0)) ]
    labels_n = [np.searchsorted(labels[i],lw[i,:,:]) for i in range(np.size(lw,0)) ]
    
    
    ## compute statistics
    pd_stats = pd.concat([pd.DataFrame(np.transpose([np.repeat(timeds[i],len(np.arange(np.max(labels_n[i])+1))),
                        np.arange(np.max(labels_n[i])+1), 
                        ndimage.sum(grid_size,
                                labels_n[i],indices_n[i]),
                        (ndimage.mean(array[i,:,:],labels_n[i],indices_n[i])),
                        (ndimage.mean(arrayvar[i,:,:],labels_n[i],indices_n[i])),
                        (ndimage.median(arrayvar[i,:,:],labels_n[i],indices_n[i])),
                        ndimage.standard_deviation(arrayvar[i,:,:],labels_n[i],indices_n[i]),
                        ndimage.maximum(arrayvar[i,:,:],labels_n[i],indices_n[i]),
                        [(ndimage.center_of_mass(array[i,:,:],
                                                labels_n[i],indices_n[i])[j][0]) for j in range(len(indices_n[i]))],
                        [(ndimage.center_of_mass(array[i,:,:],
                                                labels_n[i],indices_n[i])[j][1]) for j in range(len(indices_n[i]))],
                        [len(labels_n[i][labels_n[i]==j]) for j in np.unique(labels_n[i])]  ]),
                         columns=['time','cluster_ID','area','meanob','mean','median','std','max','com_lat','com_lon','ncells']) for i in range(np.size(labels_n,0))],
          ignore_index=False) 


    df_stats = pd_stats.drop(pd_stats[pd_stats.cluster_ID == 0].index)
    df_stats['lon'] = lon1[pd.to_numeric(df_stats.com_lon.astype(int),errors = 'coerce')]; 
    df_stats['lat'] = lat1[pd.to_numeric(df_stats.com_lat.astype(int),errors = 'coerce')]; 
    df_stats['feature'] = df_stats['meanob'].astype(int)
    df_stats = df_stats.drop(columns=['com_lat', 'com_lon'])
    df_stats = df_stats.reset_index()
        
    return(df_stats)



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