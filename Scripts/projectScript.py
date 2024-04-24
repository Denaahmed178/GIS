import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r".\project-gis\Data"
featureClasses = arcpy.ListFeatureClasses()
print(featureClasses)

# Data initialize
palaces = r".\Data\ne_10m_populated_places.shp"
countries = r".\Data\ne_10m_admin_0_countries.shp"
geographicLines = r".\Data\ne_10m_geographic_lines.shp"
disputedAreas = r".\Data\ne_10m_admin_0_disputed_areas.shp"
timeZones = r".\Data\ne_10m_time_zones.shp"
boundary_lines_land = r".\Data\ne_10m_admin_0_boundary_lines_land.shp"
Lakes = r".\Data\ne_10m_lakes.shp"

# output file
output_path = r"C:\Users\green\Desktop\project-gis\Output"
# cities & disputedAreas in Morocco

arcpy.MakeFeatureLayer_management(palaces, "Palaces_layer")
arcpy.MakeFeatureLayer_management(disputedAreas, "disputedAreas_layer")

arcpy.MakeFeatureLayer_management(countries, "Morocco_layer", """ "NAME" = 'Morocco' """)

arcpy.SelectLayerByLocation_management("Palaces_layer", "WITHIN", "Morocco_layer")
arcpy.SelectLayerByLocation_management("disputedAreas_layer", "WITHIN", "Morocco_layer")

arcpy.FeatureClassToFeatureClass_conversion("Palaces_layer", output_path, "cities_in_Morocco")
arcpy.FeatureClassToFeatureClass_conversion("disputedAreas_layer", output_path, "disputedAreas_in_Morocco")

# print the name of cities
with arcpy.da.SearchCursor("Palaces_layer", "NAME") as cities_in_Morocco_cursor:
    print ("cities in Morocco")
    for row in cities_in_Morocco_cursor:
        print(row[0])

# with arcpy.da.SearchCursor("disputedAreas_layer", "NAME") as disputedAreas_in_Morocco_cursor:
#     print ("disputed ares in Morocco")
#     for row in disputedAreas_in_Morocco_cursor:
#         print(row[0])

# lakes in africa
arcpy.MakeFeatureLayer_management(Lakes, "lakes_layer")
arcpy.MakeFeatureLayer_management(countries, "Africa_layer", """ "CONTINENT" = 'Africa' """)
arcpy.SelectLayerByLocation_management("lakes_layer", "INTERSECT", "Africa_layer")

# Count the number of selected lakes
selected_lakes_count = int(arcpy.GetCount_management("lakes_layer").getOutput(0))
print("Total number of lakes in Africa:", selected_lakes_count)

arcpy.FeatureClassToFeatureClass_conversion("lakes_layer", output_path, "lakes_in_Africa")
