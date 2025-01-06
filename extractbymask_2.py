import arcpy , shutil , os
from arcpy import env
from arcpy.sa import *

WorkSpace = "D:/jdata"
shpfile = "D:/jdata/shpfile"
Raster = "2018ChinaPOP.tif"
OutputFile = "D:/jdata/outs2"

env.workspace = "D:/jdata"

dirs = os.listdir(shpfile)                  
for i in dirs:
    # Extract files ending with .shp in the clipping features folder
    # Separate the filename and extension from the path, where the filename is [0] and the extension is [1]
    if os.path.splitext(i)[1] == ".shp":
        # Clipping feature mask path
        masks = shpfile + "/" + str(i)
        print str(i) + "Mask features successfully loaded"
        # Remove the .shp suffix from the feature name
        name = i.strip(".shp")
        # Mask extraction
        outExtractByMask = ExtractByMask(Raster, masks)
        # Save the output file
        outExtractByMask.save( OutputFile + "/" + str(name) + ".tif")
        print str(name) + "Mash extraction completed"
        print "\n"


print "-----------Mash extraction by feature field completed-----------"
