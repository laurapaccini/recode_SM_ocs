#!/bin/bash


indir="/work/mh0066/m300684/SM_experiments/m2/output_control" #fixedSM"
grid4="grid_dom03p5.nc" 
outdir="/scratch/m/m300684/uva/m2/remap/control" 
EXP1='ICON_nested_2Dland_DOM0' 
EXP3='ICON_nested_2Dsfc_DOM0'
EXP2='ICON_nested_accu_DOM0'
for i in {30..49};

 do
     cdo -P 12  -remapdis,${grid4}  ${indir}/${EXP3}3_ML_00${i}.nc ${outdir}/${EXP3}3_5km_${i}_reg.nc
     cdo -P 12  -remapdis,${grid4}  ${indir}/${EXP1}3_ML_00${i}.nc ${outdir}/${EXP1}3_5km_${i}_reg.nc
     cdo -P 12  -remapdis,${grid4}  ${indir}/${EXP2}3_ML_00${i}.nc ${outdir}/${EXP2}3_5km_${i}_reg.nc
done


#-----------------------------------------------------------------------------  
