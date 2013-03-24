This code finds the Landsat WRS-2 path/row which contains a given latitude/longitude co-ordinate.

# Dependencies #
* [GDAL/ORG](https://pypi.python.org/pypi/GDAL/)
* [Shapely](https://pypi.python.org/pypi/Shapely)
* Landsat WRS-2 Path/Row Shapefiles - download from [USGS site](http://landsat.usgs.gov/tools_wrs-2_shapefile.php), you want `wrs2_descending.zip`

# How to use #
	>>> import get_wrs
	>>> conv = ConvertToWRS()
	>>> conv.get_wrs(50.14, -1.7)
	[{'path': 202, 'row': 25}]
	>>> conv.get_wrs(50.14, -1.43)
	[{'path': 201, 'row': 25}, {'path': 202, 'row': 25}]

More details are available in the docstrings (try `ConvertToWRS?` or `conv.get_wrs?` in IPython) and in my original [blog post](#).

# License #
This code is released under the 3-clause BSD license (see the LICENSE file for more information).
