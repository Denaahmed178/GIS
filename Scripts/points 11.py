import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"....\project-gis\Data"
featureClasses = arcpy.ListFeatureClasses()
print(featureClasses)

# Data initialize
# places = r"....\project-gis\Data\ne_10m_populated_places.shp"
# countries = r"....\project-gis\Data\ne_10m_admin_0_countries.shp"
# geographicLines = r"....\project-gis\Data\ne_10m_geographic_lines.shp"
# disputedAreas = r"....\project-gis\Data\ne_10m_admin_0_disputed_areas.shp"
# timeZones = r"....\project-gis\Data\ne_10m_time_zones.shp"
# boundary_lines_land = r"....\project-gis\Data\ne_10m_admin_0_boundary_lines_land.shp"
# Lakes = r"....\project-gis\Data\ne_10m_lakes.shp"

# output file
output_path = r"....\project-gis\Output"


#############################################################################################################################

### points 11
timezone = arcpy.GetParameterAsText(0)
points = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)
zone = arcpy.GetParameterAsText(3)

arcpy.MakeFeatureLayer_management(points,"points")
timeZoneCursor = arcpy.SearchCursor(timezone,['places','time_zone','zone','FID'])
for i in timeZoneCursor:
    if i.getValue("zone") < zone:
        print (i.getValue('places'))
        print (i.getValue('time_zone')) +"\n"
        arcpy.MakeFeatureLayer_management(timezone,"timezone",""" "FID" = {} """.format(i.getValue("FID")))
        arcpy.SelectLayerByLocation_management("points","WITHIN","timezone")
        arcpy.FeatureClassToFeatureClass_conversion("points",output_path,"placesin{}".format(i.getValue("FID")))
        arcpy.AddMessage("Selecting places and timeZone successfully")
