import ogr
import shapely.geometry
import shapely.wkt

class ConvertToWRS:
    """Class which performs conversion between latitude/longitude co-ordinates
    and Landsat WRS-2 paths and rows.

    Requirements:

    * OGR (in the GDAL suite)
    * Shapely
    * Landsat WRS-2 Path/Row Shapefiles - download from USGS site
     (http://landsat.usgs.gov/tools_wrs-2_shapefile.php), you want wrs2_descending.zip

    Usage:

    1. Create an instance of the class:
        
        conv = ConvertToWRS()

    (This will take a while to run, as it loads
    the shapefiles in to memory)

    2. Use the get_wrs method to do a conversion:

        print conv.get_wrs(50.14, -1.43)

    For example:

        >>> conv = ConvertToWRS()
        >>> conv.get_wrs(50.14, -1.7)
        [{'path': 202, 'row': 25}]
        >>> conv.get_wrs(50.14, -1.43)
        [{'path': 201, 'row': 25}, {'path': 202, 'row': 25}]

    """
    def __init__(self, shapefile="./wrs2_descending.shp"):
        """Create a new instance of the ConvertToWRS class,
        and load the shapefiles into memory.

        If it can't find the shapefile then specify the path
        using the shapefile keyword - but it should work if the
        shapefile is in the same directory.
        """
        # Open the shapefile
        self.shapefile = ogr.Open(shapefile)
        # Get the only layer within it
        self.layer = self.shapefile.GetLayer(0)

        self.polygons = []

        # For each feature in the layer
        for i in range(self.layer.GetFeatureCount()):
            # Get the feature, and its path and row attributes
            feature = self.layer.GetFeature(i)
            path = feature['PATH']
            row = feature['ROW']

            # Get the geometry into a Shapely-compatible
            # format by converting to Well-known Text (Wkt)
            # and importing that into shapely
            geom = feature.GetGeometryRef()
            shape = shapely.wkt.loads(geom.ExportToWkt())

            # Store the shape and the path/row values
            # in a list so we can search it easily later
            self.polygons.append((shape, path, row))


    def get_wrs(self, lat, lon):
        """Get the Landsat WRS-2 path and row for the given
        latitude and longitude co-ordinates.

        Returns a list of dicts, as some points will be in the
        overlap between two (or more) landsat scene areas:

        [{path: 202, row: 26}, {path:186, row=7}]
        """

        # Create a point with the given latitude
        # and longitude (NB: the arguments are lon, lat
        # not lat, lon)
        pt = shapely.geometry.Point(lon, lat)
        res = []
        # Iterate through every polgon
        for poly in self.polygons:
            # If the point is within the polygon then
            # append the current path/row to the results
            # list
            if pt.within(poly[0]):
                res.append({'path': poly[1], 'row': poly[2]})

        # Return the results list to the user
        return res
