import arcpy

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"...\project-gis\Data"

# point 9
# tool for point 8
boundary_lines_land = arcpy.GetParameterAsText(1)
countries = arcpy.GetParameterAsText(0)
output_path = arcpy.GetParameterAsText(2)
country_field = arcpy.GetParameterAsText(3)
boundary_cursor = arcpy.SearchCursor(boundary_lines_land, ['ADM0_LEFT', 'ADM0_RIGHT'])

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
                                          """ "ADM0_LEFT" = '{}' OR RIGHT = COUNTRY  """.format(left_country))
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
