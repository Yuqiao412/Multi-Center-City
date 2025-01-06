# -*- coding: cp936 -*-
import os
import arcpy
import numpy as np
from arcpy.sa import *
import myfunc
import xlwt
import math
import sys


arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput=True

# arcpy.env.workspace="E:/shixi1/POP"
# newRas_path="E:/shixi1/Raster/"
# outPolygon_path="E:/shixi1/Polygon/"
# projRas_path="E:/shixi1/Raster_proj/"
# projPolygon_path="E:/shixi1/Polygon_proj/"
# outTable_path="E:/shixi1/ZonalTable/"
arcpy.env.workspace="D:/shixi/outs2"
newRas_path="D:/shixi/Raster/"
outPolygon_path="D:/shixi/Polygon/"
projRas_path="D:/shixi/Raster_proj/"
projPolygon_path="D:/shixi/Polygon_proj/"
outTable_path="D:/shixi/ZonalTable/"
sf='spatialRef.csv'
sr=arcpy.SpatialReference(4326)
#psr=arcpy.SpatialReference(32651)
count=1

def cutoff(name):
    perlist=["110000","310000","440100","440300","120000"]
    if (name in perlist):
        cut=90
    else:
        cut=95
    return cut

try:
    workbook=xlwt.Workbook()
    worksheet=workbook.add_sheet('2018Poly')
    worksheet.write(0,0,"City")
    worksheet.write(0,1,"N")
    worksheet.write(0,2,"Poly")
    
    rasters=arcpy.ListRasters('*','tif')
    for ras in rasters:
        name=ras.split(".")[0]    
        print str(count)+":"+name

        threshold=myfunc.cutoff(name)
        sfList=myfunc.spatialRef(sf)
        psr=arcpy.SpatialReference(int(sfList[name]))
        outPolygon=outPolygon_path+name+'.shp'
        projRas=projRas_path+name+'_proj.tif'
        projPolygon=projPolygon_path+name+'_proj.shp'
        outTable=outTable_path+name+'.dbf'
                          
        #Get input Raster properties
        inRas=arcpy.Raster(ras)
        no_data_value=inRas.noDataValue
        lowerLeft=arcpy.Point(inRas.extent.XMin,inRas.extent.YMin)
        cellSize=inRas.meanCellWidth
        #arcpy.env.outputCoordinateSystem=ras

        #Convert raster to array
        arr=arcpy.RasterToNumPyArray(inRas,nodata_to_value=no_data_value)

        #Calculate quantile threshold after removing null values
        newarr=arr[arr!=no_data_value]
        pt=np.percentile(newarr,threshold)

        #Select pixels greater than the threshold
        arrbool=arr>pt
        arrint=arrbool.astype('int')

        #Convert the filtered array back to a raster
        newRas = arcpy.NumPyArrayToRaster(arrint,lowerLeft,cellSize,value_to_nodata=0)
        print ("Threshol filtering completed and converted to raster- finish")
        newRas.save(newRas_path+name+'.tif')
        #Define projection for the raster
        arcpy.DefineProjection_management(newRas,sr)
        outInt=Int(newRas)
        arcpy.RasterToPolygon_conversion(outInt,outPolygon,"No_SIMPLIFY","VALUE")
        print ("Convert raster to vector")
        #Define projection for both raster and vector and export the results
        arcpy.Project_management(outPolygon,projPolygon,psr)
        arcpy.ProjectRaster_management(inRas,projRas,psr,"NEAREST","#","#","#",sr)

        with arcpy.da.UpdateCursor(projPolygon,'SHAPE@AREA') as cursor:
            for row in cursor:
                if row[0]< 3000000:
                    cursor.deleteRow()
        print ("Area filtering - finish")
        outZSaT=ZonalStatisticsAsTable(projPolygon,"FID",projRas,outTable,"DATA","SUM")
        fid=0
        fidlist=[]
        with arcpy.da.UpdateCursor(outTable,'SUM') as rows:
            for row in rows:
                if row[0]<100000:
                    fidlist.append(fid)
                    rows.deleteRow()
                fid=fid+1
        with arcpy.da.UpdateCursor(projPolygon,'FID') as cursor:
            for row in cursor:
                if row[0] in fidlist:
                    cursor.deleteRow()
        print ("Population filtering - finish")

        popsum=[row[0] for row in arcpy.da.SearchCursor(outTable,'SUM')]
        N=len(popsum)
        poparr=np.array(popsum)
        if N>1:                    
            stdpop=np.std(poparr)
            maxpop=np.max(poparr)
            poly=1-((2*stdpop)/maxpop)
        elif N<=1:
            poly=0
        print ("The number of center is："+str(N))
        print ("The centrality is："+str(poly))
                    
        worksheet.write(count,0,name)
        worksheet.write(count,1,N)
        worksheet.write(count,2,poly)
        count=count+1
        
    workbook.save('D:/shixi/2022poly.xls')
    print("done")
    
except Exception as e:
    print (e)


        
    
