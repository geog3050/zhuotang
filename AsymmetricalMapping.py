##################################################################################################
#This is a function that takes a raster data and place random points based on the grid values.
#The greater the values are, the more likely the points will be placed on the grid.
#It calculates the sum of the values of all grids, so each grid box will have an interval of its own.
#The larger the grid value is, the greater the interval will be, and therefore larger probability to
#have points placed on it. And random number is generated for the assignment of the points.
###################################################################################################
def PlacePointsWithRaster(input_geodatabase,inputRaster,numberOfPoints):
    #Environmental settings
    import arcpy
    import random
    arcpy.env.workspace = input_geodatabase
    arcpy.env.overwriteOutput = True

    #Check the existence of data
    if not inputRaster:
        return "Raster does not exist!"

    #Create points for every raster grid with the raster value
    allPoints = arcpy.conversion.RasterToPoint(inputRaster, 'pointset')

    #Get the sum of all grid values
    stats = arcpy.Statistics_analysis (allPoints,'stats',[['grid_code','SUM']])
    with arcpy.da.SearchCursor(stats, ["SUM_grid_code"]) as cursor:
        for row in cursor:
            SUM = row[0]
    del cursor, row

    #Generate random numbers from the range between 0 and the sum.
    #The length of the list is equal to the number of points should be assigned at the end.
    randomList = []
    for i in range(1,numberOfPoints+1):
        n = random.uniform(0,SUM)
        randomList.append(n)
    #Sort the list so that the list can be gone over just once
    randomList.sort()

    #This block attempts to find which point these random numbers will fall on.
    #Each raster grid value is added up one by one and compared with the random numbers.
    #If one random number falls into one of the intervals, that point associated with this interval will be exported to the final output.
    if numberOfPoints > 0:
        output = arcpy.management.CreateFeatureclass(input_geodatabase, 'output', 'POINT')
        with arcpy.da.SearchCursor(allPoints, ["OBJECTID","grid_code"]) as cursor:
            compare = 0
            pointNumber = 0
            for row in cursor:
                compare = compare + row[1]
                if compare > randomList[pointNumber]:
                    ID = row[0]
                    select = arcpy.management.SelectLayerByAttribute(allPoints, 'NEW_SELECTION', f'"OBJECTID"= {ID}')
                    arcpy.management.Append(select,output,'NO_TEST')
                    pointNumber = pointNumber + 1
                    print (pointNumber)
                    if pointNumber == numberOfPoints:
                        break
    #Delete byporducts
    del cursor, row
    arcpy.management.Delete('pointset')
    arcpy.management.Delete('stats')
    return output

######################################################################################################################
#This function is an extension of the function above which allows a polygon feature class with a field of case numbers
#and randomly place points in each polygon acoording to the raster data
######################################################################################################################
def PlacePointsWithRasterMultiplePolygons(input_geodatabase,inputRaster,inputPolygon,caseNumberFieldName):            
    #environmental settings
    import arcpy
    arcpy.env.workspace = input_geodatabase
    arcpy.env.overwriteOutput = True


    #Check the existence of data
    if not inputRaster or not inputPolygon:
        return "Data does not exist!"
    outputPoints = arcpy.management.CreateFeatureclass(input_geodatabase, 'outputPoints', 'POINT')
    with arcpy.da.SearchCursor(inputPolygon, ['OBJECTID',caseNumberFieldName]) as cursor:
        for row in cursor:
            if row[1] > 0:
                ID = row[0]
                select = arcpy.management.SelectLayerByAttribute(inputPolygon, 'NEW_SELECTION', f'"OBJECTID"= {ID}')
                #Clip the raster with each polygon
                outRaster = arcpy.management.Clip(inputRaster,'','outRaster',select,'0','ClippingGeometry')
                #Call the function defined above
                pointsOnePolygon = PlacePointsWithRaster(input_geodatabase,outRaster,row[1])
                arcpy.management.Append(pointsOnePolygon,outputPoints,'NO_TEST')

        #Delete byproducts
        del row, cursor
        arcpy.management.Delete('outRaster')
        print ('complete')

    
