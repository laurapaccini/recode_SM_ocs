from scipy import ndimage
import numpy as np
import pandas as pd


##function adapted to be used with tobac tracking 
def precip_objects(array,grid_size,rr_limit=2,area_limit=2500,stats=True,
                  s = ndimage.generate_binary_structure(2,2),lon1='',lat1='',timeds=''):
    """
    array: 3D array (time,lat,lon)
    grid_size: array with area information about the grid (cdo griddarea)
    rr_limit: threshold for precipitation rate before selecting the objects, default 1 mm hr-1
    area_limit: threshold for size of objects (reference for typical MCS size over the Amazon), default 1e4 k m-2
    s = structuring element that defines feature connections, default 8 way connection
    """
    pr_binary = np.zeros(np.shape(array))
    pr_binary[array>rr_limit] = 1
    
    lw=np.empty_like(pr_binary,dtype='int32'); num=np.empty_like(np.squeeze(pr_binary[:,0,0]),dtype='int32')
    for i in range(np.size(pr_binary,0)):
        lw[i,:,:],num[i] = ndimage.label(pr_binary[i,:,:],structure=s)
    indices = [np.arange(np.max(lw[i,:,:])+1) for i in range(np.size(lw,0)) ]
    cluster_area = [ndimage.sum(grid_size,lw[i,:,:],indices[i]) for i in range(np.size(lw,0)) ]
    mask_sizes = [cluster_area[i] < area_limit for i in range(np.size(lw,0)) ]
    removed = [mask_sizes[i][lw[i,:,:]] for i in range(np.size(lw,0)) ]
    for i in range(np.size(lw,0)):
        lw[i,:,:][removed[i]]  = 0
    ## clear and rename labels (after threshold)
    labels = [np.unique(lw[i,:,:]) for i in range(np.size(lw,0)) ]
    labels_n = [np.searchsorted(labels[i],lw[i,:,:]) for i in range(np.size(lw,0)) ]
    indices_n = [np.arange(np.max(labels_n[i])+1) for i in range(np.size(labels_n,0)) ]
    
    if stats==True:
        ## compute statistics
        pd_stats = pd.concat([pd.DataFrame(np.transpose([np.repeat(timeds[i],len(np.arange(np.max(labels_n[i])+1))),
                            np.arange(np.max(labels_n[i])+1), 
                            ndimage.sum(grid_size,
                                    labels_n[i],indices_n[i]),
                            ndimage.mean(array[i,:,:],labels_n[i],indices_n[i]),
                            (ndimage.sum(array[i,:,:],labels_n[i],indices_n[i])),
                            (ndimage.maximum(array[i,:,:],labels_n[i],indices_n[i])),
                            [int(ndimage.center_of_mass(array[i,:,:],
                                                    labels_n[i],indices_n[i])[j][0]) for j in range(len(indices_n[i]))],
                            [int(ndimage.center_of_mass(array[i,:,:],
                                                    labels_n[i],indices_n[i])[j][1]) for j in range(len(indices_n[i]))]]),
                             columns=['time','idx','area','mean','tot_prec','max_prec','y','x']) for i in range(np.size(labels_n,0))],
              ignore_index=False) 

        df_stats = pd_stats.drop(pd_stats[pd_stats.idx == 0].index)
        df_stats['longitude'] = lon1[pd.to_numeric(df_stats.x,errors = 'coerce')]; 
        df_stats['latitude'] = lat1[pd.to_numeric(df_stats.y,errors = 'coerce')]; 

    
        return(labels_n,df_stats)
    
    else:
        return(labels_n)

    

def SM_stats(arrayp,arraySM,grid_size,rr_limit=1,area_limit=5000,stats=True,
                  s = ndimage.generate_binary_structure(2,2),lon1='',lat1='',timeds=''):
    """
    arrayp, arraySM: 3D array (time,lat,lon) of precipitation and soil moisture, respectively
    grid_size: array with area information about the grid (cdo griddarea)
    rr_limit: threshold for precipitation rate before selecting the objects, default 1 mm hr-1
    area_limit: threshold for size of objects (reference for typical MCS size over the Amazon), default 1e4 k m-2
    s = structuring element that defines feature connections, default 8 way connection
    """
    pr_binary = np.zeros(np.shape(arrayp))
    pr_binary[arrayp>rr_limit] = 1
    
    lw=np.empty_like(pr_binary,dtype='int32'); num=np.empty_like(np.squeeze(pr_binary[:,0,0]),dtype='int32')
    for i in range(np.size(pr_binary,0)):
        lw[i,:,:],num[i] = ndimage.label(pr_binary[i,:,:],structure=s)
    indices = [np.arange(np.max(lw[i,:,:])+1) for i in range(np.size(lw,0)) ]
    cluster_area = [ndimage.sum(grid_size,lw[i,:,:],indices[i]) for i in range(np.size(lw,0)) ]
    mask_sizes = [cluster_area[i] < area_limit for i in range(np.size(lw,0)) ]
    removed = [mask_sizes[i][lw[i,:,:]] for i in range(np.size(lw,0)) ]
    for i in range(np.size(lw,0)):
        lw[i,:,:][removed[i]]  = 0
    ## clear and rename labels (after threshold)
    labels = [np.unique(lw[i,:,:]) for i in range(np.size(lw,0)) ]
    labels_n = [np.searchsorted(labels[i],lw[i,:,:]) for i in range(np.size(lw,0)) ]
    indices_n = [np.arange(np.max(labels_n[i])+1) for i in range(np.size(labels_n,0)) ]

   ##stats
    pd_stats = pd.concat([pd.DataFrame(np.transpose([np.repeat(timeds[i],len(np.arange(np.max(labels_n[i])+1))),
                            np.arange(np.max(labels_n[i])+1), 
                            ndimage.sum(grid_size,
                                    labels_n[i],indices_n[i]),
                            ndimage.mean(arraySM[i,:,:],labels_n[i],indices_n[i]),
                            ndimage.standard_deviation(arraySM[i,:,:],labels_n[i],indices_n[i]),
                            (ndimage.maximum(arraySM[i,:,:],labels_n[i],indices_n[i])),
                            [int(ndimage.center_of_mass(arrayp[i,:,:],
                                                    labels_n[i],indices_n[i])[j][0]) for j in range(len(indices_n[i]))],
                            [int(ndimage.center_of_mass(arrayp[i,:,:],
                                                    labels_n[i],indices_n[i])[j][1]) for j in range(len(indices_n[i]))],]),
                             columns=['time','cluster_ID','area','mean','std','max','com_lat','com_lon']) for i in range(np.size(labels_n,0))],
              ignore_index=False) 

    df_stats = pd_stats.drop(pd_stats[pd_stats.cluster_ID == 0].index)
    df_stats['lon'] = lon1[pd.to_numeric(df_stats.com_lon,errors = 'coerce')]; 
    df_stats['lat'] = lat1[pd.to_numeric(df_stats.com_lat,errors = 'coerce')]; 
    df_stats = df_stats.drop(columns=['com_lat', 'com_lon'])

       
    return(df_stats)


