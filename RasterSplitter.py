import arcpy
import os

###
def main(in_workspace, split_tiles):


    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = True
        workspace = in_workspace
        arcpy.env.workspace = arcpy.env.scratchWorkspace = workspace

    # Run CBRS
    origws = in_workspace
    arcpy.env.workspace = in_workspace
    os.chdir(in_workspace)

    # list all the folders in the input folder
    folderlist = os.listdir(in_workspace)
    arcpy.AddMessage(str(folderlist))

    for folder in folderlist:
        # change the directory to each subfolder
        current_ws = origws + "\\" + folder
        arcpy.env.workspace = current_ws

        #get the clean folder name

        # make a list of rasters
        rastfirstfour = folder[:4]
        rawrasters = arcpy.ListRasters(rastfirstfour +"*")
        arcpy.AddMessage(rawrasters)
        rawrasters.remove()

        # make the directories for the splits
        count = 0
        while int(count) <= (int(split_tiles) - 1):
            os.mkdir((origws + "\\" + "s_" + str(folder) + "_" + str(count)))
            arcpy.AddMessage((origws + "\\" + "s_" + str(folder) + "_" + str(count)) + " has been created ...")
            count = count + 1

        splits_folder = origws + "\\" + 'split'
        os.mkdir((splits_folder))
        arcpy.AddMessage(splits_folder + "has been created ...")

        # get the gausian raster
        gaus_index = rasters.index("*g3")
        gaus_rast = rasters[gaus_index]
        arcpy.AddMessage("splitting " + str(gaus_rast))
        arcpy.SplitRaster_management(gaus_rast, splits_folder, "gaus_ " + str(folder), "NUMBER_OF_TILES", \
                                     "GRID", "BILINEAR", "2 2", "#", "4", "PIXELS", \
                                     "#", "#")
        rasters.remove(gaus_rast)


        # get the raw raster
        z = str(rasters)
        zclean = z[3:-2]
        raw_index = rasters.index(zclean)
        raw_rast = rasters[raw_index]
        arcpy.AddMessage("splitting " + str(raw_rast))
        arcpy.SplitRaster_management(raw_rast, splits_folder, "raw_ " + str(folder), "NUMBER_OF_TILES", \
                                     "GRID", "BILINEAR", "2 2", "#", "4", "PIXELS", \
                                     "#", "#")
        rasters.remove(raw_rast)

        # place the rasters into their named folders
        arcpy.env.workspace = splits_folder

        raw_splits = arcpy.ListRasters("raw_*")
        gaus_splits = arcpy.ListRasters("gaus_*")

        for raster in raw_splits:
            foldername = "s_" + raster[5:]
            arcpy.AddMessage("copying " + str(raster) + " to " + str(foldername))
            arcpy.CopyRaster_management(raster, foldername)

        for raster in gaus_splits:
            foldername = "s_" + raster[6:]
            arcpy.AddMessage("copying " + str(raster) + " to " + str(foldername))
            arcpy.CopyRaster_management(raster, foldername)


###
if __name__ == "__main__":
    in_workspace = arcpy.GetParameterAsText(0)
    split_tiles = arcpy.GetParameterAsText(1)

    main(in_workspace, split_tiles)
###