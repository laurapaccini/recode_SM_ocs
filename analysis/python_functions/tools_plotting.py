import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.pyplot import figure
import matplotlib.gridspec as gridspec
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


#### define colormaps
whiteTOblueTOgreen = LinearSegmentedColormap.from_list('mycmap',
                                                ['white','#ece2f0','#d0d1e6','#a6bddb','#67a9cf',
                                                '#3690c0','#02818a','#016c59','#014636'])

brownTOwhiteTOgreen = LinearSegmentedColormap.from_list('mycmap', 
                                          ['#543005','#8c510a',
                                          '#bf812d','#dfc27d','white','white',
                                           '#80cdc1','#35978f','#01665e','#003c30'])
blueTOwhiteTOred =  LinearSegmentedColormap.from_list('mycmap', 
                                          ['#053061','#2166ac','#4393c3','#92c5de','#d1e5f0',
                                           'white','white','#fddbc7','#f4a582','#d6604d','#b2182b',
                                              '#67001f'])
whiteTOblueTOgreenToPurple = LinearSegmentedColormap.from_list('mycmap',
                                                ['white','#ece2f0','#d0d1e6','#a6bddb','#67a9cf',
                                                '#3690c0','#02818a','#016c59','#542788',
                                                 '#c51b7d'])

spectral_cyclic = LinearSegmentedColormap.from_list('mycmap',
                                                ['#9e0142', '#5e4fa2','#3288bd', '#66c2a5','#abdda4',
                                            '#e6f598','#ffffbf','#fee08b','#fdae61','#f46d43','#d53e4f','#9e0142',])

## Map style
def map_style(dax, title1='',
                     yl=True, xb = True, yloc = np.arange(-30,21,10), xloc = [-90,-75,-20,15,70],
                     ylimi=-10, ylimf=21, xlimi=-82, xlimf=20,cc='k',sz=11,title_loc='left',
             hor='horizontal',pd=0.03):  
   
    dax.set_ylim(ylimi,ylimf); dax.set_xlim(xlimi,xlimf)
    dax.coastlines(resolution='50m',color=cc)
    dax.set_title(title1, loc=title_loc)
    gl = dax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
              linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False; gl.right_labels = False;
    gl.bottom_labels = xb;  gl.left_labels = yl;
    gl.xformatter = LONGITUDE_FORMATTER ; gl.yformatter = LATITUDE_FORMATTER
    gl.ylocator = mticker.FixedLocator(yloc);  gl.xlocator = mticker.FixedLocator(xloc)
    gl.xlabel_style = {'size': sz, 'color': 'black'}; gl.ylabel_style = {'size': sz, 'color': 'black'}