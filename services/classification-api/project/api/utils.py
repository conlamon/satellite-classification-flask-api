import math


def deg_to_num(lat_deg, lng_deg, zoom):
    '''
    Helper function to convert lat/lon to x,y coords for image tiles
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
    https://gist.github.com/tmcw/4954720 -- For final conversion to MBTiles format

    Input:  lat_deg -- float; Latitude value for specified point
            lng_deg -- float; Longitudinal value specified point
            zoom -- int; The zoom value for the specified point

    Output: xtile -- int; The integer value specifying the x tile number
            ytile -- int; The integer value specifying the y tile number

    '''
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lng_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

    # Need to convert Y coord to TMS format, since using MBTiles
    ytile = (2 ** zoom) - ytile - 1

    return xtile, ytile
