import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r".\project-gis\Data"
featureClasses = arcpy.ListFeatureClasses()
print(featureClasses)

# Data initialize
#place
places = r".\Data\ne_10m_populated_places.shp"
countries = r".\Data\ne_10m_admin_0_countries.shp"
geographicLines = r".\Data\ne_10m_geographic_lines.shp"
disputedAreas = r".\Data\ne_10m_admin_0_disputed_areas.shp"
timeZones = r".\Data\ne_10m_time_zones.shp"
boundary_lines_land = r".\Data\ne_10m_admin_0_boundary_lines_land.shp"
Lakes = r".\Data\ne_10m_lakes.shp"

# output file
output_path = r".\project-gis\Output"

# point(2) cities & disputedAreas in Morocco
arcpy.MakeFeatureLayer_management(places, "Places_layer")
arcpy.MakeFeatureLayer_management(disputedAreas, "disputedAreas_layer")

arcpy.MakeFeatureLayer_management(countries, "Morocco_layer", """ "NAME" = 'Morocco' """)

arcpy.SelectLayerByLocation_management("Places_layer", "WITHIN", "Morocco_layer")
arcpy.SelectLayerByLocation_management("disputedAreas_layer", "WITHIN", "Morocco_layer")

arcpy.FeatureClassToFeatureClass_conversion("Places_layer", output_path, "cities_in_Morocco")
arcpy.FeatureClassToFeatureClass_conversion("disputedAreas_layer", output_path, "disputedAreas_in_Morocco")

# print the name of cities
with arcpy.da.SearchCursor("Places_layer", "NAME") as cities_in_Morocco_cursor:
    print ("cities in Morocco")
    for row in cities_in_Morocco_cursor:
        print(row[0])

# with arcpy.da.SearchCursor("disputedAreas_layer", "NAME") as disputedAreas_in_Morocco_cursor:
#     print ("disputed ares in Morocco")
#     for row in disputedAreas_in_Morocco_cursor:
#         print(row[0])

# point(3) lakes in africa
arcpy.MakeFeatureLayer_management(Lakes, "lakes_layer")
arcpy.MakeFeatureLayer_management(countries, "Africa_layer", """ "CONTINENT" = 'Africa' """)
arcpy.SelectLayerByLocation_management("lakes_layer", "INTERSECT", "Africa_layer")

# Count the number of selected lakes
selected_lakes_count = int(arcpy.GetCount_management("lakes_layer").getOutput(0))
print("Total number of lakes in Africa:", selected_lakes_count)

arcpy.FeatureClassToFeatureClass_conversion("lakes_layer", output_path, "lakes_in_Africa")

##point 4
# Create a shapefile for cities that have SOV0NAME equals United Kingdom.
arcpy.MakeFeatureLayer_management(places,'Places_layer',""" "SOV0NAME"='United Kingdom' """)
arcpy.FeatureClassToFeatureClass_conversion('Places_layer',output,'United Kingdom cities')

###point 5
uk=r"D:\4th year\Second smester\GIS\Gislabs\Output\United Kingdom cities.shp"
# Using the Update Cursor update SOV0NAME fields to Britain in uk shape ile .
with arcpy.da.UpdateCursor(uk, ['SOV0NAME']) as cursor:
    for row in cursor:
        row[0] = 'Britain'
        cursor.updateRow(row)
        print(row[0])
#point6
# print the name,scalerank & wikidataid for all lakes.
cities_cursor=arcpy.SearchCursor(Lakes,['name','scalerank','wikidataid'])
for lake in cities_cursor:
    print(lake.getValue('name'))
    print(lake.getValue('scalerank'))
    print(lake.getValue('wikidataid')) +"\n"
###################
# point 7
# arcpy.MakeFeatureLayer_management(Lakes,'lake')
lakes_cursor=arcpy.UpdateCursor(Lakes, ['wikidataid','note'])
for x in lakes_cursor:
    if x.getValue('wikidataid')=='':
        x.setValue('wikidataid',"undefined")
        x.setValue('note', "this row is updated")
        lakes_cursor.updateRow(x)
        #print(x[1])
 arcpy.FeatureClassToFeatureClass_conversion('lake', output_path, 'cities_in{}'.format(x.getValue('note')))
        #rint x.getValue('note')

# point 8
countries_fields = ['Germany', 'Egypt', 'Brazil']

# Create a search cursor for the boundary lines
boundary_cursor = arcpy.SearchCursor(boundary_lines_land, ['ADM0_LEFT', 'ADM0_LEFT'])

# Iterate through the search cursor and create shapefiles for the left and right borders
for row in boundary_cursor:

    left_country = row.getValue("ADM0_LEFT")  # Get the value of the 'ADMO_LEFT' field
    right_country = row.getValue("ADM0_RIGHT")  # Get the value of the 'ADMO_RIGHT' field
    # Check if the left country is in the list of countries
    if left_country in countries_fields:
        # Generate a unique feature layer name for the left country
        left_layer_name = 'Left_' + left_country.replace(" ",
                                                         "_")  # Replace spaces with underscores for valid layer name
        # Create a feature layer for the left country
        arcpy.MakeFeatureLayer_management(boundary_lines_land, left_layer_name,
                                          """ "ADM0_LEFT" = '{}'""".format(left_country))
        # Convert the feature layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion(left_layer_name, output_path, 'left_border_{}'.format(left_country))

    # Check if the right country is in the list of countries
    if right_country in countries_fields:
        # Generate a unique feature layer name for the right country
        right_layer_name = 'Right_' + right_country.replace(" ",
                                                            "_")  # Replace spaces with underscores for valid layer name
        # Create a feature layer for the right country
        arcpy.MakeFeatureLayer_management(boundary_lines_land, right_layer_name,
                                          """ "ADM0_RIGHT" = '{}'""".format(right_country))
        # Convert the feature layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion(right_layer_name, output_path,
                                                    'right_border_{}'.format(right_country))
# point 9
# tool for point 8
boundary_lines_land = arcpy.GetParameterAsText(1)
countries = arcpy.GetParameterAsText(0)
output_path = arcpy.GetParameterAsText(2)
country_field = arcpy.GetParameterAsText(3)
boundary_cursor = arcpy.SearchCursor(boundary_lines_land, ['ADM0_LEFT', 'ADM0_LEFT'])

# Iterate through the search cursor and create shapefiles for the left and right borders
for row in boundary_cursor:

    left_country = row.getValue("ADM0_LEFT")  # Get the value of the 'ADMO_LEFT' field
    right_country = row.getValue("ADM0_RIGHT")  # Get the value of the 'ADMO_RIGHT' field
    # Check if the left country is in the list of countries
    if left_country in country_field:
        # Generate a unique feature layer name for the left country
        left_layer_name = 'Left_' + left_country.replace(" ",
                                                         "_")  # Replace spaces with underscores for valid layer name
        # Create a feature layer for the left country
        arcpy.MakeFeatureLayer_management(boundary_lines_land, left_layer_name,
                                          """ "ADM0_LEFT" = '{}'""".format(left_country))
        # Convert the feature layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion(left_layer_name, output_path, 'left_border_{}'.format(left_country))

    # Check if the right country is in the list of countries
    if right_country in country_field:
        # Generate a unique feature layer name for the right country
        right_layer_name = 'Right_' + right_country.replace(" ",
                                                            "_")  # Replace spaces with underscores for valid layer name
        # Create a feature layer for the right country
        arcpy.MakeFeatureLayer_management(boundary_lines_land, right_layer_name,
                                          """ "ADM0_RIGHT" = '{}'""".format(right_country))
        # Convert the feature layer to a shapefile
        arcpy.FeatureClassToFeatureClass_conversion(right_layer_name, output_path,
                                                    'right_border_{}'.format(right_country))

arcpy.AddMessage("the boundries has been printed ")
#############################################################################################################################

### points 10,11
timezone = arcpy.GetParameterAsText(0)
# r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_time_zones.shp'
points = arcpy.GetParameterAsText(1)
#r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_populated_places.shp'
countries = r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_admin_0_countries.shp'
output = arcpy.GetParameterAsText(2)
zone = arcpy.GetParameterAsText(3)
#r'D:\4th Year\2nd semester\GIS\GIS\output'

arcpy.MakeFeatureLayer_management(points,"points")
timeZoneCursor = arcpy.SearchCursor(timezone,['places','time_zone','zone','FID'])
for i in timeZoneCursor:
    if i.getValue("zone") < float(0):
        print (i.getValue('places'))
        print (i.getValue('time_zone')) +"\n"
        arcpy.MakeFeatureLayer_management(timezone,"timezone",""" "FID" = {} """.format(i.getValue("FID")))
        arcpy.SelectLayerByLocation_management("points","WITHIN","timezone")
        arcpy.FeatureClassToFeatureClass_conversion("points",output,"placesin{}".format(i.getValue("FID")))
        arcpy.AddMessage("success")

###################################################################################################################

### point 12
countries = r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_admin_0_countries.shp'
cities = r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_populated_places.shp'
equator = r'D:\4th Year\2nd semester\GIS\GIS\data\ne_10m_geographic_lines.shp'
output = r'D:\4th Year\2nd semester\GIS\GIS\output'

arcpy.MakeFeatureLayer_management(countries,"countries")
arcpy.MakeFeatureLayer_management(cities,"cities")
# equatorCursor = arcpy.SearchCursor(equator,['name'])
# for i in equatorCursor:

arcpy.MakeFeatureLayer_management(equator,"equator",""" "name" = 'Equator' """)

arcpy.SelectLayerByLocation_management("countries","INTERSECT","equator")
arcpy.SelectLayerByLocation_management("cities","INTERSECT","equator")

print(arcpy.FeatureClassToFeatureClass_conversion("countries",output,"countriesInEq"))
print(arcpy.FeatureClassToFeatureClass_conversion("cities", output, "citiesInEq"))
###################################################################################################################
# points 13,14
#import arcpy
import re
#arcpy.env.workspace = r"C:\Users\lenovo\Desktop\project\Data"
#arcpy.env.overwriteOutput = True
#time = r"C:\Users\lenovo\Desktop\project\Data\ne_10m_time_zones.shp"
#output = r"C:\Users\lenovo\Desktop\project\output"
time = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)
places_list = []
#timezone_list = ['UTC+02:00', 'UTC-02:00']
cities_cursor = arcpy.SearchCursor(time, ['places', 'time_zone'])
for i in cities_cursor:
    if i.getValue('time_zone') == 'UTC+02:00':
        print(i.getValue('places'))
        places_list.append(i.getValue('places'))
#print('no repetition ')
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
    #print(place)

################################################################################################################################################
### points 15,16,17,18

img_folder = r'F:\ArcGis-content\images'

import os
from PIL import Image, ExifTags

img_contents = os.listdir(img_folder)

for image in img_contents:
    print (image)
    full_path = os.path.join(img_folder,image)
    print (full_path)
    pillow_img = Image.open(full_path)
    exif = {ExifTags.TAGS[k]: v for k , v in pillow_img.getexif().items() if k in ExifTags.TAGS}
    print (exif )
    gps_all = {}
    try:
        for key in exif['GPSInfo'].keys():
            decoded_value = ExifTags.GPSTAGS.get(key)
            gps_all[decoded_value]=exif['GPSInfo'][key]

        long_ref = gps_all.get('GPSLongitudeRef')
        longitude = gps_all.get('GPSLongitude')
        lat_ref = gps_all.get('GPSLatitudeRef')
        latitude = gps_all.get('GPSLatitude')

        print (long_ref , "   ",longitude)
        print (lat_ref, "   ", latitude)

    except:
        print ("This image has no GPS info {}".format(full_path))
        pass


