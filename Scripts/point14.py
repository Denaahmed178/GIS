import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"...\project-gis\Data"
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
###################################################################################################################
# point 14
import re

time = arcpy.GetParameterAsText(0)

#output = arcpy.GetParameterAsText(1)
places_list = []

cities_cursor = arcpy.SearchCursor(time, ['places', 'time_zone'])
for i in cities_cursor:
    if i.getValue('time_zone') == 'UTC+02:00':
        print(i.getValue('places'))
        places_list.append(i.getValue('places'))

unique_places = []
for place in places_list:
    # Split the string into individual countries
    countries = re.split(r', | and ', place)
    unique_places.extend(countries)
final_unique_places = []
for place in unique_places:
    if place not in final_unique_places:
        final_unique_places.append(place)
for place in final_unique_places:
    arcpy.AddMessage(place)
