def PercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2):
    #environmental settings
    import arcpy
    arcpy.env.workspace = input_geodatabase
    arcpy.env.overwriteOutput = True

    #Getting the feature types of the input feature classes and raise error if not both are polygons
    desc1 = arcpy.Describe(fcPolygon1)
    desc2 = arcpy.Describe(fcPolygon2)
    if desc1.shapeType != 'Polygon' or desc2.shapeType != 'Polygon':
        raise TypeError('Input feature type needs to be polygon')
    else:

        #Calculate area for fcPolygon2
        arcpy.AddField_management(fcPolygon2,'area_sqmi','DOUBLE')
        arcpy.CalculateGeometryAttributes_management(fcPolygon2, [['area_sqmi','AREA_GEODESIC']],'MILES_US')

        #Create intersections
        arcpy.Intersect_analysis([fcPolygon2,fcPolygon1],'intersections')

        #Calculate area for fcPolygon1 intersections
        arcpy.AddField_management('intersections','area_sqmi_inter','DOUBLE')
        arcpy.CalculateGeometryAttributes_management('intersections', [['area_sqmi_inter','AREA_GEODESIC']],'MILES_US')

        #Dissolve intersections by fcPolygon2 and calculate sum for areas
        arcpy.Dissolve_management('intersections', 'interDissolve',[f'FID_{fcPolygon2}'],[['area_sqmi_inter','SUM']],'MULTI_PART')

        #Attach the area field to the original fcPolygon2
        arcpy.management.JoinField(fcPolygon2,'OBJECTID','interDissolve',f'FID_{fcPolygon2}','SUM_area_sqmi_inter')

        #Replaceing nulls with zeros
        cursor = arcpy.UpdateCursor(fcPolygon2)
        for row in cursor:
            if row.SUM_area_sqmi_inter == None:
                row.SUM_area_sqmi_inter = 0
                cursor.updateRow(row)
        del row
        
