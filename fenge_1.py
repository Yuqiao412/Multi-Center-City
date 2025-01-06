import arcpy , shutil , os
from arcpy import env
from arcpy.sa import *


WorkSpace = "D:/SpatiotemporalBigData/Experiment"
FieldFeature = "D:/SpatiotemporalBigData/UrbanBoundary/ChinaCity.shp"
Field = "shiCode"
Raster = "chn_ppp_2020.tif"
OutputFile = "D:/SpatiotemporalBigData/Experiment/outstwo"
Free = raw_input("----------- Press Enter to start execution -----------")

print "\n"
# set the workspace
arcpy.env.workspace = WorkSpace
# set the temporary folder path
TempFile = WorkSpace + "/" + "shpfile"
# Split features
arcpy.Split_analysis(FieldFeature , FieldFeature , Field , TempFile)
