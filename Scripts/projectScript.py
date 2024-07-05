import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"C:\Users\green\Desktop\project-gis\Data"
featureClasses = arcpy.ListFeatureClasses()
print(featureClasses)

# Data initialize
places = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_populated_places.shp"
countries = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_admin_0_countries.shp"
geographicLines = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_geographic_lines.shp"
disputedAreas = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_admin_0_disputed_areas.shp"
timeZones = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_time_zones.shp"
boundary_lines_land = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_admin_0_boundary_lines_land.shp"
Lakes = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_lakes.shp"

# output file
output_path = r"C:\Users\green\Desktop\project-gis\Output"

# point(2) cities & disputedAreas in Morocco
arcpy.MakeFeatureLayer_management(places, "Places_layer")
arcpy.MakeFeatureLayer_management(disputedAreas, "disputedAreas_layer")

arcpy.MakeFeatureLayer_management(countries, "Morocco_layer", """ "NAME" = 'Morocco' """)

arcpy.SelectLayerByLocation_management("Places_layer", "WITHIN", "disputedAreas_layer")
arcpy.SelectLayerByLocation_management("disputedAreas_layer", "WITHIN", "Morocco_layer")

arcpy.FeatureClassToFeatureClass_conversion("Places_layer", output_path, "cities_in_Morocco")
arcpy.FeatureClassToFeatureClass_conversion("disputedAreas_layer", output_path, "disputedAreas_in_Morocco")


# print the name of cities
with arcpy.da.SearchCursor("Places_layer", "NAME") as cities_in_Morocco_cursor:
    print ("cities in Morocco")
    for row in cities_in_Morocco_cursor:
        print(row[0])

with arcpy.da.SearchCursor("disputedAreas_layer", "NAME") as disputedAreas_in_Morocco_cursor:
    print ("disputed ares in Morocco")
    for row in disputedAreas_in_Morocco_cursor:
        print(row[0])

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
arcpy.FeatureClassToFeatureClass_conversion('Places_layer',output_path,'United Kingdom cities')

# ###point 5
uk=r"C:\Users\green\Desktop\project-gis\Output\United Kingdom cities.shp"
# Using the Update Cursor update SOV0NAME fields to Britain in uk shape ile .
with arcpy.da.UpdateCursor(uk, ['SOV0NAME']) as cursor:
    for row in cursor:
        row[0] = 'Britain'
        cursor.updateRow(row)
        #print(row[0])
#point6
# print the name,scalerank & wikidataid for all lakes.
Lakes_cursor = arcpy.SearchCursor(Lakes,['name','scalerank','wikidataid'])
for lake in Lakes_cursor:
    print("name",lake.getValue('name'))
    print("scalerank",lake.getValue('scalerank'))
    print("wikidataid",lake.getValue('wikidataid'))
    print ("\n")
###################
# point 7
#arcpy.MakeFeatureLayer_management(Lakes,'lake')
# Update cursor to iterate through the rows
with arcpy.da.UpdateCursor(Lakes, ["wikidataid", "note"]) as cursor:
    for row in cursor:
        if row[0] == ' ':  # If wikidataid is null
            row[0] = "undefined"  # Update wikidataid
            row[1] = "This row is updated"  # Add note
            cursor.updateRow(row)  # Update the row
         #print(x[1])
# point 8
countries_fields = ['Germany', 'Egypt', 'Brazil']

# Create a search cursor for the boundary lines
boundary_cursor = arcpy.SearchCursor(boundary_lines_land, ['ADM0_LEFT', 'ADM0_RIGHT'])

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
###################################################################################################################

## point 10

arcpy.MakeFeatureLayer_management(places,"points")
timeZoneCursor = arcpy.SearchCursor(timeZones,['places','time_zone','zone','FID'])
for i in timeZoneCursor:
    if i.getValue("zone") < 0:
        print (i.getValue('places'))
        print (i.getValue('time_zone')) +"\n"
        arcpy.MakeFeatureLayer_management(timeZones,"timezone",""" "FID" = {} """.format(i.getValue("FID")))
        arcpy.SelectLayerByLocation_management("points","WITHIN","timezone")
        arcpy.FeatureClassToFeatureClass_conversion("points",output_path,"placesin{}".format(i.getValue("FID")))


###################################################################################################################
### point 12
arcpy.MakeFeatureLayer_management(countries,"countries")
arcpy.MakeFeatureLayer_management(places,"cities")

arcpy.MakeFeatureLayer_management(geographicLines,"equator",""" "name" = 'Equator' """)

arcpy.SelectLayerByLocation_management("countries","INTERSECT","equator")
arcpy.SelectLayerByLocation_management("cities","WITHIN","countries")

countries_eq = arcpy.FeatureClassToFeatureClass_conversion("countries",output_path,"countriesInEq")
cities_eq = arcpy.FeatureClassToFeatureClass_conversion("cities", output_path, "citiesInEq")

with arcpy.da.SearchCursor(countries_eq, "NAME") as cursor:
    print("Countries intersecting with the Equator:")
    for row in cursor:
        print(row[0])

with arcpy.da.SearchCursor(cities_eq, "NAME") as cursor:
    print("Cities intersecting with the Equator:")
    for row in cursor:
        print(row[0])
###################################################################################################################
# points 13
import re
timeZones = r"C:\Users\green\Desktop\project-gis\Data\ne_10m_time_zones.shp"
places_list = []
#timezone_list = ['UTC+02:00', 'UTC-02:00']
cities_cursor = arcpy.SearchCursor(timeZones, ['places', 'time_zone'])
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
print("places in the time Zone")
for place in final_unique_places:
    print(place)
################################################################################################################################################
### points 15,16,17,18

img_folder = r'C:\Users\green\Desktop\project-gis\images'

import os
from PIL import Image, ExifTags

img_contents = os.listdir(img_folder)

for image in img_contents:
    print (image)
    full_path = os.path.join(img_folder,image)
    print (full_path)
    pillow_img = Image.open(full_path)
    exif = {ExifTags.TAGS[k]: v for k , v in pillow_img.getexif().items() if k in ExifTags.TAGS}
    print (exif)
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


