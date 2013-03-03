import ogr
import shapely.geometry
import shapely.wkt

class ConvertToWRS:
    """Class which performs conversion between latitude/longitude co-ordinates
    and Landsat WRS-2 paths and rows.

    Requirements:

    * OGR (in the GDAL suite)
    * Shapely

    Usage:

    1. Create an instance of the class:
        
        conv = ConvertToWRS()

    (This will take a while to run, as it loads the shapefiles in to memory)

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
        """Create a new instance of the ConvertToWRS class, and load the shapefiles into memory.

        If it can't find the shapefile then specify the path using the shapefile keyword - but it
        should work if the shapefile is in the same directory.
        """
        self.shapefile = ogr.Open(shapefile)
        self.layer = self.shapefile.GetLayer(0)

        self.polygons = []

        for i in range(self.layer.GetFeatureCount()):
            feature = self.layer.GetFeature(i)
            path = feature['PATH']
            row = feature['ROW']
            geom = feature.GetGeometryRef()
            shape = shapely.wkt.loads(geom.ExportToWkt())
            self.polygons.append((shape, path, row))


    def get_wrs(self, lat, lon):
        """Get the Landsat WRS-2 path and row for the given latitude and longitude co-ordinates.

        Returns a list of dicts, as some points will be in the overlap between two (or more)
        landsat scene areas:

        [{path: 202, row: 26}, {path:186, row=7}]
        """

        pt = shapely.geometry.Point(lon, lat)
        res = []
        for poly in self.polygons:
            if pt.within(poly[0]):
                res.append({'path': poly[1], 'row': poly[2]})

        return res