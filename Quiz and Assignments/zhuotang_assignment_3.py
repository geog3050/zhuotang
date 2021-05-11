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
    return(["AustinTang", "zhuotang"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
import arcpy
def printFeatureClassNames(workspace):
    arcpy.env.workspace = workspace
    fcList = arcpy.ListFeatureClasses()
    #Get the information of each feature class
    for i in fcList:
        desc = arcpy.da.Describe(i)
        print(i + ' is a ' + desc['shapeType'] + ' feature class')

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    arcpy.env.workspace = workspace
    fieldList = arcpy.ListFields(inputFc)
    #Select numerical fields and print values
    for field in fieldList:
        if (field.type == 'Integer' or field.type == 'Float' or field.type == 'Double'):
            print(field.name,field.type)


###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

######################################################################
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    import os
    arcpy.env.workspace = input_geodatabase
    outWorkspace = output_geodatabase
    Type = shapeType
    # Use ListFeatureClasses to generate a list of shapefiles in the
    #  workspace shown above.
    fcList = arcpy.ListFeatureClasses('*',f'{Type}')
    # Execute CopyFeatures for each input shapefile
    for shapefile in fcList:
        # Determine the new output feature class path and name
        out_featureclass = os.path.join(outWorkspace, 
                                    os.path.splitext(shapefile)[0])
        arcpy.CopyFeatures_management(shapefile, out_featureclass)

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    arcpy.env.workspace = workspace
    # Join the feature layer to a table
    val_res = arcpy.ValidateJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
    matched = int(val_res[0]) 
    row_count = int(val_res[1])
    # Validate the join returns matched rows before proceeding
    if matched >= 1:
        joined = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
        # Copy the joined layer to a new permanent feature class
        arcpy.CopyFeatures_management(joined, outFeatures)
    print(f"Output Features: {outFeatures} had matches {matched} and created {row_count} records")


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
