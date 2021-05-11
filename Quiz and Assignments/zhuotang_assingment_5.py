###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Austin Tang", "zhuotang"])

###################################################################### 
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute, geodatabase = "assignment2.gdb"):
    import arcpy
    import os
    arcpy.env.workspace = geodatabase
    arcpy.env.overwriteOutput = True
    fc = fcpolygon

    # Check the existence of the feature class
    if not fc:
        return "Feature class does not exist!"
        
    #check the input type
    describeFc = arcpy.Describe(fc)
    if describeFc.ShapeType != 'Polygon':
        return 'Incorrect input feature type!'

    #check the existence of the attribute name
    fieldnamesFc = [f.name for f in arcpy.ListFields(fc)]
    if attribute not in fieldnamesFc:
        return 'The attribute is not in field names!'
    else:
        arcpy.AddField_management(fc, 'density_sqm', 'FLOAT')

    #check the projection system
    if describeFc.spatialReference.PCSCode == 0:
        print ('WARNING: the projection is a geographic coordinate system, which will be converted to Albers projection for area calculation')
    #calculate area
    arcpy.AddField_management(fc,'size','FLOAT')
    arcpy.CalculateField_management(fc, 'size', '!shape.area@squaremiles!','PYTHON3')

    #calcylate the density
    updatecursor = arcpy.da.UpdateCursor(fc, ['size', attribute, 'density_sqm'])
    for row in updatecursor:
        row[2] = row[1] / row[0] 
        updatecursor.updateRow(row)
        del row
    del updatecursor

###################################################################### 
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase = "assignment2.gdb"):
    import arcpy
    import os
    arcpy.env.workspace = geodatabase
    arcpy.env.overwriteOutput = True
    fcp = fcClipPolygon
    fcl = fcLine

    #Check the existence of the clip polygon
    clipPoly = arcpy.SelectLayerByAttribute_management(fcp, "NEW_SELECTION", f"{polygonIDFieldName} = '{clipPolygonID}'")
    count = arcpy.GetCount_management(clipPoly)
    if count[0] == '0':
        return 'The polygon does not exist, check the input clipPolygonID!'

    #check whether the projections are the same
    if arcpy.Describe(fcp).spatialReference.name != arcpy.Describe(fcl).spatialReference.name:
        arcpy.Project_management(fcl, "fclProjected", arcpy.Describe(fcp).spatialReference)

    fclClip = arcpy.Clip_analysis(fcl,clipPoly,'fclClip','')

    #add a field for the cut output
    arcpy.AddField_management(fclClip, "length", "FLOAT")
    #calculate the length in miles
    arcpy.CalculateField_management(fclClip, "length", '!shape.length@miles!', "PYTHON3")

    #Calculate the sum
    searchcursor = arcpy.da.SearchCursor(fclClip, ["length"])
    suma = 0.0
    for row in searchcursor:
        suma = suma + row[0]
        del row
    del searchcursor

    return suma

    

    

######################################################################
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):
    import arcpy
    import os
    arcpy.env.workspace = geodatabase
    arcpy.env.overwriteOutput = True

    #check the existence of a projected coordinate system
    if arcpy.Describe(fcPoint).spatialReference.PCSCode == 0:
        print ('WARNING: the projection is a geographic coordinate system.')

    #Generate point distance table in the given unit and the given distance threshold
    pointDistance = arcpy.PointDistance_analysis(fcPoint, fcPoint, 'PointDis', str(distance)+ " "+ distanceUnit)

    
    #create a list in the length of "fcPoint" and store the count of each point in the list
    length = int(arcpy.GetCount_management(fcPoint).getOutput(0))
    countList = [0] * length
    searchcursor = arcpy.da.SearchCursor(pointDistance, ['INPUT_FID'])
    for row in searchcursor:
       countList[row[0] - 1] = countList[row[0] - 1] + 1
       del row
    del searchcursor

    #Append the countlist to the attribute table
    fieldname = 'countOfPoints'
    arcpy.AddField_management(fcPoint, fieldname, 'SHORT')
    updatecursor = arcpy.da.UpdateCursor(fcPoint, [fieldname])
    i = 0
    for row in updatecursor:
        row[0] = countList[i]
        updatecursor.updateRow(row)
        i = i + 1
        del row
    del updatecursor
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
