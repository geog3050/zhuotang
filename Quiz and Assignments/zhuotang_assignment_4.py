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
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    #environmental settings
    import arcpy
    arcpy.env.workspace = input_geodatabase
    arcpy.env.overwriteOutput = True
    
    #Getting the feature types of the input feature classes and raise error if not both are polygons
    desc1 = arcpy.Describe(fcPoint)
    desc2 = arcpy.Describe(fcPolyline)
    if desc1.shapeType != 'Point' or desc2.shapeType != 'Polyline':
        raise TypeError('Incorrect input feature types')
    else:
        # Calculate the distance to the nearest line feature
        arcpy.analysis.Near(fcPoint, fcPolyline)
    
    

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    #environmental settings
    import arcpy
    arcpy.env.workspace = input_geodatabase
    arcpy.env.overwriteOutput = True
    
    #Getting the feature types of the input feature classes and raise error if not both are polygons
    desc1 = arcpy.Describe(fcPoint)
    desc2 = arcpy.Describe(fcPolygon)
    if desc1.shapeType != 'Point' or desc2.shapeType != 'Polygon':
        raise TypeError('Incorrect input feature types')
    else:
        selectedPoints = arcpy.SelectLayerByAttribute_management(fcPoint, 'NEW_SELECTION', f"{pointFieldName} = '{pointFieldValue}'")
        arcpy.CopyFeatures_management(selectedPoints,'selectedPoints')
        arcpy.analysis.SpatialJoin(fcPolygon, selectedPoints, 'outputJoin', '#', '#', 'Count','CONTAINS')
        arcpy.management.JoinField(fcPolygon,'OBJECTID','outputJoin','OBJECTID',['Join_Count'])

        #cleaning unecessary files
        arcpy.management.Delete('outputJoin')
        arcpy.management.Delete('selectedPoints')

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    #environmental settings
    import arcpy
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    
    #Getting the feature types of the input feature classes and raise error if not both are polygons
    desc1 = arcpy.Describe(fcPoint)
    desc2 = arcpy.Describe(fcPolygon)
    if desc1.shapeType != 'Point' or desc2.shapeType != 'Polygon':
        raise TypeError('Incorrect input feature types')
    else:

        #Get unique values from the field and convert to list so it supports indexing
        nameList = list(set(row[0] for row in arcpy.da.SearchCursor(fcPoint, f"{pointFieldName}")))
        
        #Truncate the values in the field
        shortName = [x.replace(' ','') for x in nameList]
        shortNames = [y[:13] for y in shortName]

        #go through the list
        a = 0
        for i in shortNames:
            #get the original name for SelectByAttribute
            j = nameList[a]
            a = a+1

            #Select by attribute and spatial join
            selectedPoints = arcpy.SelectLayerByAttribute_management(fcPoint, 'NEW_SELECTION', f"{pointFieldName} = '{j}'")
            arcpy.CopyFeatures_management(selectedPoints,'selectedPoints')
            arcpy.analysis.SpatialJoin(fcPolygon, selectedPoints, 'outputJoin', '#', '#', 'Count','CONTAINS')

            #Change the field name 'Join_Count' to its corresponding short name
            arcpy.management.AlterField('outputJoin','Join_Count',f'{i}',f'{i}')

            #Attach the field to the original polygon
            arcpy.management.JoinField(fcPolygon,'OBJECTID','outputJoin','OBJECTID',[f'{i}'])

            #cleaning unecessary files
            arcpy.management.Delete('outputJoin')
            arcpy.management.Delete('selectedPoints')

        
        
        




######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
